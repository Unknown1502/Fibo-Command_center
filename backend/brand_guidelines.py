"""
Brand Guidelines System - Store and enforce brand identity across generations.
Validates colors, styles, and visual consistency for professional tools.
"""

import json
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path
import re

logger = logging.getLogger(__name__)


class BrandGuideline:
    """Represents a brand guideline profile."""
    
    def __init__(
        self,
        brand_id: str,
        name: str,
        colors: Optional[List[str]] = None,
        fonts: Optional[List[str]] = None,
        styles: Optional[List[str]] = None,
        rules: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.brand_id = brand_id
        self.name = name
        self.colors = colors or []
        self.fonts = fonts or []
        self.styles = styles or []
        self.rules = rules or {}
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'brand_id': self.brand_id,
            'name': self.name,
            'colors': self.colors,
            'fonts': self.fonts,
            'styles': self.styles,
            'rules': self.rules,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BrandGuideline':
        """Create from dictionary."""
        return cls(**data)


class BrandGuidelineManager:
    """
    Manages brand guidelines and validates generations against brand rules.
    Stores brand profiles per project for consistent visual identity.
    """
    
    def __init__(self, storage_path: str = './brand_guidelines'):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)
        self.guidelines: Dict[str, BrandGuideline] = {}
        self._load_all()
    
    def _load_all(self):
        """Load all stored guidelines."""
        for file in self.storage_path.glob('*.json'):
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                    guideline = BrandGuideline.from_dict(data)
                    self.guidelines[guideline.brand_id] = guideline
                logger.info(f"Loaded brand guideline: {guideline.name}")
            except Exception as e:
                logger.error(f"Failed to load {file}: {str(e)}")
    
    def create_guideline(
        self,
        brand_id: str,
        name: str,
        colors: Optional[List[str]] = None,
        fonts: Optional[List[str]] = None,
        styles: Optional[List[str]] = None,
        rules: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> BrandGuideline:
        """Create and store a new brand guideline."""
        guideline = BrandGuideline(
            brand_id=brand_id,
            name=name,
            colors=colors,
            fonts=fonts,
            styles=styles,
            rules=rules,
            metadata=metadata
        )
        
        self.guidelines[brand_id] = guideline
        self._save_guideline(guideline)
        
        logger.info(f"Created brand guideline: {name} ({brand_id})")
        return guideline
    
    def _save_guideline(self, guideline: BrandGuideline):
        """Save guideline to disk."""
        file_path = self.storage_path / f"{guideline.brand_id}.json"
        with open(file_path, 'w') as f:
            json.dump(guideline.to_dict(), f, indent=2)
    
    def get_guideline(self, brand_id: str) -> Optional[BrandGuideline]:
        """Retrieve a brand guideline."""
        return self.guidelines.get(brand_id)
    
    def list_guidelines(self) -> List[Dict[str, Any]]:
        """List all brand guidelines."""
        return [
            {
                'brand_id': g.brand_id,
                'name': g.name,
                'colors_count': len(g.colors),
                'fonts_count': len(g.fonts),
                'styles_count': len(g.styles),
                'rules_count': len(g.rules)
            }
            for g in self.guidelines.values()
        ]
    
    def update_guideline(
        self,
        brand_id: str,
        **updates
    ) -> Optional[BrandGuideline]:
        """Update an existing guideline."""
        guideline = self.guidelines.get(brand_id)
        if not guideline:
            return None
        
        for key, value in updates.items():
            if hasattr(guideline, key) and value is not None:
                setattr(guideline, key, value)
        
        self._save_guideline(guideline)
        logger.info(f"Updated brand guideline: {brand_id}")
        return guideline
    
    def delete_guideline(self, brand_id: str) -> bool:
        """Delete a brand guideline."""
        if brand_id not in self.guidelines:
            return False
        
        # Delete file
        file_path = self.storage_path / f"{brand_id}.json"
        if file_path.exists():
            file_path.unlink()
        
        # Remove from memory
        del self.guidelines[brand_id]
        logger.info(f"Deleted brand guideline: {brand_id}")
        return True
    
    def validate_generation(
        self,
        brand_id: str,
        parameters: Dict[str, Any],
        image_analysis: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Validate generation parameters against brand guidelines.
        
        Returns:
            Dictionary with compliance score, violations, and suggestions
        """
        guideline = self.get_guideline(brand_id)
        if not guideline:
            return {
                'valid': False,
                'error': f'Brand guideline not found: {brand_id}'
            }
        
        violations = []
        warnings = []
        score = 100
        
        # Check style compliance
        if guideline.styles:
            requested_style = parameters.get('style')
            if requested_style and requested_style not in guideline.styles:
                violations.append({
                    'field': 'style',
                    'requested': requested_style,
                    'allowed': guideline.styles,
                    'severity': 'high'
                })
                score -= 20
        
        # Check color palette compliance
        if guideline.colors:
            requested_palette = parameters.get('color_palette')
            # If brand specifies allowed palettes in rules
            allowed_palettes = guideline.rules.get('allowed_color_palettes', [])
            if allowed_palettes and requested_palette not in allowed_palettes:
                violations.append({
                    'field': 'color_palette',
                    'requested': requested_palette,
                    'allowed': allowed_palettes,
                    'severity': 'medium'
                })
                score -= 15
        
        # Check lighting rules
        lighting_rules = guideline.rules.get('lighting', {})
        if lighting_rules:
            requested_lighting = parameters.get('lighting')
            forbidden_lighting = lighting_rules.get('forbidden', [])
            if requested_lighting in forbidden_lighting:
                violations.append({
                    'field': 'lighting',
                    'requested': requested_lighting,
                    'reason': 'Lighting style forbidden by brand guidelines',
                    'severity': 'high'
                })
                score -= 20
        
        # Check composition rules
        composition_rules = guideline.rules.get('composition', {})
        if composition_rules:
            requested_composition = parameters.get('composition')
            required_composition = composition_rules.get('required')
            if required_composition and requested_composition != required_composition:
                warnings.append({
                    'field': 'composition',
                    'message': f'Brand prefers {required_composition} composition',
                    'severity': 'low'
                })
                score -= 5
        
        # Overall compliance determination
        compliance_level = 'excellent' if score >= 90 else \
                          'good' if score >= 75 else \
                          'acceptable' if score >= 60 else \
                          'poor'
        
        return {
            'valid': score >= 60,  # 60% minimum compliance
            'compliance_score': score,
            'compliance_level': compliance_level,
            'violations': violations,
            'warnings': warnings,
            'suggestions': self._generate_suggestions(guideline, violations, warnings),
            'brand_name': guideline.name
        }
    
    def _generate_suggestions(
        self,
        guideline: BrandGuideline,
        violations: List[Dict],
        warnings: List[Dict]
    ) -> List[str]:
        """Generate helpful suggestions based on violations."""
        suggestions = []
        
        if violations:
            suggestions.append(f" Found {len(violations)} compliance violation(s)")
        
        for violation in violations:
            field = violation.get('field')
            if field == 'style' and guideline.styles:
                suggestions.append(f"Use approved styles: {', '.join(guideline.styles)}")
            elif field == 'color_palette':
                allowed = violation.get('allowed', [])
                if allowed:
                    suggestions.append(f"Use approved palettes: {', '.join(allowed)}")
        
        if not violations and warnings:
            suggestions.append(f" Compliant with {len(warnings)} minor warning(s)")
        
        if not violations and not warnings:
            suggestions.append(" Fully compliant with brand guidelines")
        
        return suggestions
    
    def parse_document(self, document_text: str) -> Dict[str, Any]:
        """
        Parse a brand guideline document (simple text parsing).
        In production, this would use NLP or specific parsers for PDF/DOCX.
        
        Args:
            document_text: Text content of brand document
        
        Returns:
            Parsed guideline data
        """
        parsed = {
            'colors': [],
            'fonts': [],
            'styles': [],
            'rules': {}
        }
        
        # Extract hex colors
        color_pattern = r'#[0-9A-Fa-f]{6}'
        parsed['colors'] = list(set(re.findall(color_pattern, document_text)))
        
        # Extract common font names (simple approach)
        common_fonts = ['Arial', 'Helvetica', 'Roboto', 'Open Sans', 'Montserrat', 
                        'Lato', 'Georgia', 'Times New Roman', 'Verdana']
        for font in common_fonts:
            if font.lower() in document_text.lower():
                parsed['fonts'].append(font)
        
        # Extract style keywords
        style_keywords = {
            'minimalist': ['minimal', 'simple', 'clean', 'modern'],
            'vintage': ['vintage', 'retro', 'classic', 'nostalgic'],
            'cinematic': ['cinematic', 'dramatic', 'film', 'movie'],
            'realistic': ['realistic', 'photographic', 'natural']
        }
        
        for style, keywords in style_keywords.items():
            if any(kw in document_text.lower() for kw in keywords):
                parsed['styles'].append(style)
        
        return parsed


# Global instance
brand_manager = BrandGuidelineManager()
