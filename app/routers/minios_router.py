from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from minio import Minio
from minio.error import S3Error
from app.common.middleware import verificar_acceso
from app.common.settings import (
    MINIO_ENDPOINT,
    MINIO_ACCESS_KEY,
    MINIO_SECRET_KEY,
    MINIO_BUCKET_NAME,
    MINIO_SECURE
)
import uuid
import os
from datetime import datetime, timedelta

router = APIRouter()

def get_minio_client():
    """Crea y retorna un cliente MinIO"""
    return Minio(
        endpoint=MINIO_ENDPOINT,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=MINIO_SECURE
    )

def ensure_bucket_exists(client: Minio, bucket_name: str):
    """Asegura que el bucket exista, lo crea si no existe"""
    try:
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
            print(f"Bucket '{bucket_name}' creado exitosamente")
    except S3Error as e:
        print(f"Error al crear bucket: {e}")
        raise HTTPException(status_code=500, detail=f"Error al crear bucket: {str(e)}")

def validate_minio_connection():
    """Valida la conexión a MinIO y las credenciales"""
    try:
        client = get_minio_client()
        list(client.list_buckets())
        return True, "Conexión exitosa"
    except S3Error as e:
        return False, f"Error de MinIO: {str(e)}"
    except Exception as e:
        return False, f"Error de conexión: {str(e)}"

@router.post("/minios/upload")
async def upload_file(
    _: None = Depends(verificar_acceso),
    file: UploadFile = File(...),
):
    """
    Endpoint para subir archivos a MinIO
    
    Args:
        file: Archivo a subir
        
    Returns:
        dict: Información del archivo subido
    """
    try:
        if not file:
            raise HTTPException(status_code=400, detail="No se proporcionó ningún archivo")
        
        max_size = 10 * 1024 * 1024 
        if file.size and file.size > max_size:
            raise HTTPException(
                status_code=413, 
                detail=f"El archivo es demasiado grande. Tamaño máximo: {max_size/1024/1024}MB"
            )
        
        client = get_minio_client()
        
        ensure_bucket_exists(client, MINIO_BUCKET_NAME)
        
        file_extension = os.path.splitext(file.filename)[1] if file.filename else ""
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        
        file_content = await file.read()
        
        from io import BytesIO
        client.put_object(
            bucket_name=MINIO_BUCKET_NAME,
            object_name=unique_filename,
            data=BytesIO(file_content),
            length=len(file_content),
            content_type=file.content_type or "application/octet-stream"
        )
        
        file_url = f"{'https' if MINIO_SECURE else 'http'}://{MINIO_ENDPOINT}/{MINIO_BUCKET_NAME}/{unique_filename}"
        
        return {
            "mensaje": "Archivo subido exitosamente",
            "archivo": {
                "nombre_original": file.filename,
                "nombre_guardado": unique_filename,
                "tamaño": len(file_content),
                "tipo_contenido": file.content_type,
                "bucket": MINIO_BUCKET_NAME,
                "url": file_url,
                "fecha_subida": datetime.now().isoformat()
            }
        }
        
    except S3Error as e:
        raise HTTPException(status_code=500, detail=f"Error de MinIO: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.post("/minios/upload-to-folder")
async def upload_file_to_folder(
    folder_name: str,
    _: None = Depends(verificar_acceso),
    file: UploadFile = File(...),
):
    """
    Endpoint para subir archivos a una carpeta específica en MinIO
    
    Args:
        folder_name: Nombre de la carpeta donde se guardará el archivo
        file: Archivo a subir
        
    Returns:
        dict: Información del archivo subido
    """
    try:
        if not file:
            raise HTTPException(status_code=400, detail="No se proporcionó ningún archivo")
        
        if not folder_name or not folder_name.strip():
            raise HTTPException(status_code=400, detail="Debe especificar el nombre de la carpeta")
        
        folder_name = folder_name.strip().replace('\\', '/').strip('/')
        
        max_size = 10 * 1024 * 1024 
        if file.size and file.size > max_size:
            raise HTTPException(
                status_code=413, 
                detail=f"El archivo es demasiado grande. Tamaño máximo: {max_size/1024/1024}MB"
            )
        
        client = get_minio_client()
        
        ensure_bucket_exists(client, MINIO_BUCKET_NAME)
        
        file_extension = os.path.splitext(file.filename)[1] if file.filename else ""
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        
        full_object_name = f"{folder_name}/{unique_filename}"
        
        file_content = await file.read()
        
        from io import BytesIO
        client.put_object(
            bucket_name=MINIO_BUCKET_NAME,
            object_name=full_object_name,
            data=BytesIO(file_content),
            length=len(file_content),
            content_type=file.content_type or "application/octet-stream"
        )
        
        file_url = f"{'https' if MINIO_SECURE else 'http'}://{MINIO_ENDPOINT}/{MINIO_BUCKET_NAME}/{full_object_name}"
        
        return {
            "mensaje": "Archivo subido exitosamente",
            "archivo": {
                "nombre_original": file.filename,
                "nombre_guardado": unique_filename,
                "carpeta": folder_name,
                "ruta_completa": full_object_name,
                "tamaño": len(file_content),
                "tipo_contenido": file.content_type,
                "bucket": MINIO_BUCKET_NAME,
                "url": file_url,
                "fecha_subida": datetime.now().isoformat()
            }
        }
        
    except S3Error as e:
        raise HTTPException(status_code=500, detail=f"Error de MinIO: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/minios/get-file")
async def get_file(
    path: str,
    expires_days: int = 7,  
    _: None = Depends(verificar_acceso)
):
    """
    Endpoint para obtener un archivo específico de MinIO con URL pre-firmada
    
    Args:
        path: Ruta del archivo a obtener (query parameter)
        expires_days: Número de días para que expire la URL (por defecto 7 días)
        
    Returns:
        dict: Información del archivo con URL firmada que expira
    """
    try:
        is_connected, connection_message = validate_minio_connection()
        if not is_connected:
            raise HTTPException(
                status_code=500, 
                detail=f"Error de conexión a MinIO: {connection_message}"
            )
        
        client = get_minio_client()
        
        if not client.bucket_exists(MINIO_BUCKET_NAME):
            raise HTTPException(status_code=404, detail="El bucket no existe")

        try:
            stat = client.stat_object(MINIO_BUCKET_NAME, path)
        except S3Error as e:
            if e.code == "NoSuchKey":
                raise HTTPException(status_code=404, detail="El archivo no existe")
            raise

        try:
            expiring_url = client.presigned_get_object(
                MINIO_BUCKET_NAME, 
                path, 
                expires=timedelta(days=expires_days)
            )
            
            expiry_date = datetime.now() + timedelta(days=expires_days)
            
            return {
                "tipo_contenido": stat.content_type,
                "url_firmada": expiring_url,
                "fecha_expiracion": expiry_date.isoformat(),
            }
            
        except S3Error as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Error generando URL firmada: {str(e)}"
            )

    except S3Error as e:
        error_detail = f"Error de MinIO: {str(e)}"
        if hasattr(e, 'code'):
            if e.code == "SignatureDoesNotMatch":
                error_detail += " - Verifica las credenciales ACCESS_KEY y SECRET_KEY"
            elif e.code == "InvalidAccessKeyId":
                error_detail += " - ACCESS_KEY inválido"
            elif e.code == "NoSuchKey":
                error_detail = "El archivo no existe"
        
        raise HTTPException(status_code=500, detail=error_detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/minios/connection-bucket-test")
async def test_minio_connection():
    """
    Endpoint para probar la conexión a MinIO y validar credenciales
    
    Returns:
        dict: Estado de la conexión y configuración
    """
    is_connected, message = validate_minio_connection()
    
    return {
        "conexion_exitosa": is_connected,
        "mensaje": message,
        "configuracion": {
            "endpoint": MINIO_ENDPOINT,
            "bucket": MINIO_BUCKET_NAME,
            "secure": MINIO_SECURE,
            "access_key": MINIO_ACCESS_KEY[:8] + "..." if MINIO_ACCESS_KEY else None,
        }
    }

@router.get("/minios/list-images")
async def list_images_with_expiring_urls(
    expires_hours: int = 24, 
    # dependencies=[Depends(verificar_acceso)]  # Descomenta si quieres usar autenticación
):
    """
    Endpoint para listar imágenes en MinIO con URLs con expiración
    
    Args:
        expires_hours: Número de horas para que expire la URL (por defecto 24 horas)
        
    Returns:
        dict: Lista de imágenes con URLs pre-firmadas que expiran
    """
    try:
        is_connected, connection_message = validate_minio_connection()
        if not is_connected:
            raise HTTPException(
                status_code=500, 
                detail=f"Error de conexión a MinIO: {connection_message}"
            )
        
        client = get_minio_client()
        
        if not client.bucket_exists(MINIO_BUCKET_NAME):
            return {"imagenes": [], "mensaje": "El bucket no existe"}
        
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.svg', '.ico'}
        
        objects = client.list_objects(MINIO_BUCKET_NAME)
        
        images_list = []
        failed_urls = []
        
        for obj in objects:
            file_extension = os.path.splitext(obj.object_name)[1].lower()
            if file_extension in image_extensions:
                try:
                    expiring_url = client.presigned_get_object(
                        MINIO_BUCKET_NAME, 
                        obj.object_name, 
                        expires=timedelta(hours=expires_hours)
                    )
                    
                    expiry_date = datetime.now() + timedelta(hours=expires_hours)
                    
                    images_list.append({
                        "nombre": obj.object_name,
                        "tamaño": obj.size,
                        "fecha_modificacion": obj.last_modified.isoformat() if obj.last_modified else None,
                        "etag": obj.etag,
                        "extension": file_extension,
                        "url_con_expiracion": expiring_url,
                        "fecha_expiracion": expiry_date.isoformat(),
                        "horas_expiracion": expires_hours
                    })
                except S3Error as e:
                    failed_urls.append({
                        "archivo": obj.object_name,
                        "error": str(e),
                        "codigo": getattr(e, 'code', 'Unknown')
                    })
                    print(f"Error generando URL para {obj.object_name}: {e}")
                    continue
                except Exception as e:
                    failed_urls.append({
                        "archivo": obj.object_name,
                        "error": str(e),
                        "codigo": "UnknownError"
                    })
                    print(f"Error inesperado para {obj.object_name}: {e}")
                    continue
        
        response = {
            "imagenes": images_list,
            "total": len(images_list),
            "bucket": MINIO_BUCKET_NAME,
            "configuracion": {
                "horas_expiracion": expires_hours,
                "extensiones_validas": list(image_extensions)
            }
        }
        
        if failed_urls:
            response["errores"] = {
                "urls_fallidas": failed_urls,
                "total_errores": len(failed_urls)
            }
        
        return response
        
    except S3Error as e:
        error_detail = f"Error de MinIO: {str(e)}"
        if hasattr(e, 'code'):
            if e.code == "SignatureDoesNotMatch":
                error_detail += " - Verifica las credenciales ACCESS_KEY y SECRET_KEY"
            elif e.code == "InvalidAccessKeyId":
                error_detail += " - ACCESS_KEY inválido"
            elif e.code == "SignatureDoesNotMatch":
                error_detail += " - SECRET_KEY inválido o endpoint incorrecto"
        
        raise HTTPException(status_code=500, detail=error_detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.delete("/minios/delete-file/{filename}")
async def delete_file(
    filename: str,
    _: None = Depends(verificar_acceso)
):
    """
    Endpoint para eliminar un archivo de MinIO
    
    Args:
        filename: Nombre del archivo a eliminar
        
    Returns:
        dict: Confirmación de eliminación
    """
    try:
        client = get_minio_client()
        
        if not client.bucket_exists(MINIO_BUCKET_NAME):
            raise HTTPException(status_code=404, detail="El bucket no existe")
        
        client.remove_object(MINIO_BUCKET_NAME, filename)
        
        return {
            "mensaje": "Archivo eliminado exitosamente",
            "archivo": filename,
            "bucket": MINIO_BUCKET_NAME
        }
        
    except S3Error as e:
        if e.code == "NoSuchKey":
            raise HTTPException(status_code=404, detail="El archivo no existe")
        raise HTTPException(status_code=500, detail=f"Error de MinIO: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")