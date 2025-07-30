from pydantic import BaseModel, Field
from typing import Optional, List, Literal

class CTAButton(BaseModel):
    text: str
    url: Optional[str] = None
    variant: Literal['primary', 'secondary'] = 'primary'

class Feature(BaseModel):
    title: str
    description: str
    icon: Optional[str] = None

class Testimonial(BaseModel):
    name: str
    role: str
    content: str
    avatar: Optional[str] = None
    rating: Optional[float] = Field(default=None, ge=0, le=5)

class FinalCTA(BaseModel):
    title: str
    description: Optional[str] = None
    primaryButton: CTAButton
    secondaryButton: Optional[CTAButton] = None

class HeroSection(BaseModel):
    title: str
    subtitle: str
    backgroundImage: Optional[str] = None
    ctaButtons: List[CTAButton]

class FeaturesSection(BaseModel):
    title: Optional[str] = None
    subtitle: Optional[str] = None
    items: List[Feature]

class TestimonialsSection(BaseModel):
    title: str
    items: List[Testimonial]

class Theme(BaseModel):
    primaryColor: str = '#4f46e5'
    secondaryColor: str = '#7c3aed'
    textColor: str = '#1f2937'
    backgroundColor: str = '#ffffff'

class Enterprice(BaseModel):
    hero: HeroSection
    features: FeaturesSection
    testimonials: Optional[TestimonialsSection] = None
    finalCta: FinalCTA
    theme: Optional[Theme] = None
