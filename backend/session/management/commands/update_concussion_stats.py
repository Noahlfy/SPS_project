from django.core.management.base import BaseCommand
from backend.data_handler import update_concussion_stats_for_impact

class Command(BaseCommand):
    help = 'Update concussion stats based on simulated impact data'

    def add_arguments(self, parser):
        parser.add_argument('session_id', type=int, help='ID de la session pour laquelle mettre à jour les stats')

    def handle(self, *args, **kwargs):
        session_id = kwargs['session_id']
        self.stdout.write(self.style.SUCCESS(f'Starting update for session ID {session_id}'))
        
        try:
            update_concussion_stats_for_impact(session_id)
            self.stdout.write(self.style.SUCCESS('Update completed successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
