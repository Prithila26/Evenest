"""
Management command to assign images to products and services.

This command maps product/service titles to image files in the media folder
following a configurable mapping strategy. It updates the database with image paths.

Usage:
    python manage.py assign_product_images [--dry-run] [--verbose]

Options:
    --dry-run:  Show what would be done without making changes
    --verbose:  Show detailed progress information
"""

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from pathlib import Path
import os
from core.models import (
    EventManagement, Photography, Catering, PrintingService, StoreItem
)


class ImageMapper:
    """Maps product/service titles to image filenames."""
    
    def __init__(self):
        """Initialize image mapper with existing media files."""
        self.media_root = Path(settings.MEDIA_ROOT)
        self.services_dir = self.media_root / 'services'
        self.store_dir = self.media_root / 'store'
        
        # Cache existing image files
        self.service_images = self._get_image_files(self.services_dir)
        self.store_images = self._get_image_files(self.store_dir)
        
    def _get_image_files(self, directory):
        """Get list of image files in a directory."""
        if not directory.exists():
            return []
        return [f.name for f in directory.glob('*') if f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif']]
    
    def map_event_management(self, event):
        """Map EventManagement service to image file."""
        mapping = {
            'Royal Wedding': 'event_management_1_5ooqnmO.jpeg',
            'Wedding': 'event_management_1.jpeg',
            'Corporate': 'event_management_2.jpeg',
            'Birthday': 'event_management_1.jpeg',
            'Engagement': 'event_management_2.jpeg',
        }
        
        for key, img in mapping.items():
            if key.lower() in event.title.lower():
                return f'services/{img}'
        
        # Default based on event_type
        if event.event_type == 'Wedding':
            return 'services/event_management_1.jpeg'
        elif event.event_type == 'Corporate':
            return 'services/event_management_2.jpeg'
        else:
            return 'services/event_management_1.jpeg'
    
    def map_photography(self, photo):
        """Map Photography service to image file."""
        mapping = {
            'Wedding': 'photography_agency_1.jpeg',
            'Pre-Wedding': 'photography_agency_2.jpeg',
            'Birthday': 'photography_agency_1.jpeg',
            'Corporate': 'photography_agency_2.jpeg',
            'Mehendi': 'photography_agency_1.jpeg',
            'Portrait': 'photography_agency_2.jpeg',
            'Drone': 'photography_agency_1.jpeg',
            'Videography': 'photography_agency_2.jpeg',
        }
        
        for key, img in mapping.items():
            if key.lower() in photo.title.lower():
                return f'services/{img}'
        
        # Default based on shoot_type
        return 'services/photography_agency_1.jpeg'
    
    def map_catering(self, catering):
        """Map Catering service to image file."""
        mapping = {
            'Bengali': 'catering_services_1.jpeg',
            'Continental': 'catering_services_2.jpeg',
            'Biryani': 'catering_services_1.jpeg',
            'Mughlai': 'catering_services_1.jpeg',
            'Vegetarian': 'catering_services_2.jpeg',
            'Chinese': 'catering_services_1.jpeg',
            'BBQ': 'catering_services_2.jpeg',
            'Dessert': 'catering_services_1.jpeg',
            'Appetizers': 'catering_services_2.jpeg',
        }
        
        for key, img in mapping.items():
            if key.lower() in catering.title.lower() or key.lower() in catering.cuisine_type.lower():
                return f'services/{img}'
        
        # Alternate between images
        return 'services/catering_services_1.jpeg'
    
    def map_printing(self, printing):
        """Map PrintingService to image file."""
        mapping = {
            'Wedding': 'card_printers_1.jpeg',
            'Card': 'card_printers_1.jpeg',
            'Invitation': 'card_printers_2.jpeg',
            'Business': 'card_printers_1.jpeg',
            'Banner': 'card_printers_2.jpeg',
            'Menu': 'card_printers_1.jpeg',
            'Name Tag': 'card_printers_2.jpeg',
        }
        
        for key, img in mapping.items():
            if key.lower() in printing.title.lower() or key.lower() in printing.print_type.lower():
                return f'services/{img}'
        
        return 'services/card_printers_1.jpeg'
    
    def map_store_item(self, item):
        """Map StoreItem to image file."""
        category_mapping = {
            'Decor Items': 'decor_items_1.jpeg',
            'Event Accessories': 'event_accesories_1.jpeg',
            'Wedding Supplies': 'wedding_supply_1.jpeg',
            'Lighting': 'event_accesories_2.jpeg',
            'Floral': 'decor_items_2.jpeg',
            'Table': 'decor_items_1.jpeg',
            'Gift': 'event_accesories_1.jpeg',
        }
        
        # Try to match by item name
        name_keywords = {
            'floral': 'decor_items_2.jpeg',
            'light': 'event_accesories_2.jpeg',
            'table': 'decor_items_1.jpeg',
            'chair': 'event_accesories_1.jpeg',
            'candle': 'decor_items_1.jpeg',
            'balloon': 'event_accesories_2.jpeg',
            'rose': 'decor_items_2.jpeg',
            'decor': 'decor_items_1.jpeg',
            'gift': 'event_accesories_1.jpeg',
            'prop': 'event_accesories_2.jpeg',
        }
        
        item_name_lower = item.name.lower()
        for keyword, img in name_keywords.items():
            if keyword in item_name_lower:
                return f'store/{img}'
        
        # Fall back to category
        category_name = item.category.name
        for cat_key, img in category_mapping.items():
            if cat_key.lower() in category_name.lower():
                return f'store/{img}'
        
        # Default
        return 'store/decor_items_1.jpeg'


class Command(BaseCommand):
    """
    Assign images to products and services.
    
    This command creates a mapping between product/service titles and existing
    image files in the media folder, then updates the database.
    """
    
    help = 'Assign images to all products and services based on mapping rules'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without making changes',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed progress information',
        )
    
    def handle(self, *args, **options):
        dry_run = options['dry_run']
        verbose = options['verbose']
        
        mapper = ImageMapper()
        
        # Summary statistics
        stats = {
            'eventmanagement': {'total': 0, 'updated': 0},
            'photography': {'total': 0, 'updated': 0},
            'catering': {'total': 0, 'updated': 0},
            'printing': {'total': 0, 'updated': 0},
            'storeitem': {'total': 0, 'updated': 0},
        }
        
        # Process EventManagement
        self.stdout.write(self.style.SUCCESS('Processing EventManagement...'))
        for event in EventManagement.objects.all():
            stats['eventmanagement']['total'] += 1
            image_path = mapper.map_event_management(event)
            
            if event.image != image_path:
                if verbose:
                    self.stdout.write(f'  Event: {event.title} -> {image_path}')
                if not dry_run:
                    event.image = image_path
                    event.save(update_fields=['image'])
                stats['eventmanagement']['updated'] += 1
        
        # Process Photography
        self.stdout.write(self.style.SUCCESS('Processing Photography...'))
        for photo in Photography.objects.all():
            stats['photography']['total'] += 1
            image_path = mapper.map_photography(photo)
            
            if photo.image != image_path:
                if verbose:
                    self.stdout.write(f'  Photo: {photo.title} -> {image_path}')
                if not dry_run:
                    photo.image = image_path
                    photo.save(update_fields=['image'])
                stats['photography']['updated'] += 1
        
        # Process Catering
        self.stdout.write(self.style.SUCCESS('Processing Catering...'))
        for catering in Catering.objects.all():
            stats['catering']['total'] += 1
            image_path = mapper.map_catering(catering)
            
            if catering.image != image_path:
                if verbose:
                    self.stdout.write(f'  Catering: {catering.title} -> {image_path}')
                if not dry_run:
                    catering.image = image_path
                    catering.save(update_fields=['image'])
                stats['catering']['updated'] += 1
        
        # Process PrintingService
        self.stdout.write(self.style.SUCCESS('Processing PrintingService...'))
        for printing in PrintingService.objects.all():
            stats['printing']['total'] += 1
            image_path = mapper.map_printing(printing)
            
            if printing.image != image_path:
                if verbose:
                    self.stdout.write(f'  Printing: {printing.title} -> {image_path}')
                if not dry_run:
                    printing.image = image_path
                    printing.save(update_fields=['image'])
                stats['printing']['updated'] += 1
        
        # Process StoreItem
        self.stdout.write(self.style.SUCCESS('Processing StoreItem...'))
        for item in StoreItem.objects.all():
            stats['storeitem']['total'] += 1
            image_path = mapper.map_store_item(item)
            
            if item.image != image_path:
                if verbose:
                    self.stdout.write(f'  StoreItem: {item.name} -> {image_path}')
                if not dry_run:
                    item.image = image_path
                    item.save(update_fields=['image'])
                stats['storeitem']['updated'] += 1
        
        # Print summary
        self.stdout.write(self.style.SUCCESS('\n=== Image Assignment Summary ==='))
        for model_name, counts in stats.items():
            total = counts['total']
            updated = counts['updated']
            self.stdout.write(
                f'{model_name:20} | Total: {total:3} | Updated: {updated:3}'
            )
        
        total_all = sum(s['total'] for s in stats.values())
        updated_all = sum(s['updated'] for s in stats.values())
        self.stdout.write(self.style.SUCCESS(f'\nTotal Records: {total_all} | Total Updated: {updated_all}'))
        
        if dry_run:
            self.stdout.write(self.style.WARNING('\n⚠️  DRY RUN: No changes were made to the database.'))
            self.stdout.write('Run without --dry-run to apply changes.')
