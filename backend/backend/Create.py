from django.utils import timezone
from datetime import timedelta
import random
from session_stats.models import SessionStats

from datetime import timedelta
import random
from django.utils import timezone

def update_session_stats_for_impact(session_id, max_g_impact=3.0, post_impact_decay=0.1, min_pace=5.0, max_pace=12.0, max_bpm=180, impact_duration=5):
    """
    Met à jour les valeurs de session-stats pour simuler un impact lors d'une session, en utilisant la valeur maximale de G-force pour détecter l'impact.

    Args:
    - session_id: ID de la session à modifier.
    - max_g_impact: Valeur maximale de la G-force lors de l'impact.
    - post_impact_decay: Taux de décroissance de la G-force après l'impact.
    - min_pace: Vitesse minimale du joueur en km/h avant l'impact.
    - max_pace: Vitesse maximale du joueur en km/h avant l'impact.
    - max_bpm: BPM maximum lors de l'impact.
    - impact_duration: Durée de l'impact en secondes.
    """

    # Récupérer les stats pour la session donnée
    stats = SessionStats.objects.filter(session_id=session_id).order_by('time')
    if not stats.exists():
        print("Aucune donnée trouvée pour cette session.")
        return

    # Identifier le point d'impact comme étant le moment du pic de G-force
    max_g_stat = stats.order_by('-g').first()
    if not max_g_stat or max_g_stat.g < 0.5:  # Ignorer si G-force maximale est très faible
        print("Pas de pic de G-force significatif trouvé pour simuler un impact.")
        return

    impact_time = max_g_stat.time  # Temps du pic de G-force
    pre_impact_pace = random.uniform(min_pace, max_pace)
    pre_impact_bpm = random.randint(80, 100)

    for stat in stats:
        # Calculer le temps écoulé par rapport au moment de l'impact
        elapsed_time = (stat.time - impact_time).total_seconds()

        # Ajuster les valeurs en fonction de l'impact
        if abs(elapsed_time) <= impact_duration:
            # Pendant l'impact
            stat.g = max_g_impact * (1 - abs(elapsed_time) / impact_duration)
            stat.BPM = min(max_bpm, pre_impact_bpm + (max_bpm - pre_impact_bpm) * (1 - abs(elapsed_time) / impact_duration))
            stat.pace = pre_impact_pace * (1 - abs(elapsed_time) / impact_duration)
        elif elapsed_time > impact_duration:
            # Après l'impact - décroissance de la G-force et stabilisation des autres valeurs
            stat.g = max(0, stat.g - post_impact_decay)
            stat.BPM = max(pre_impact_bpm, stat.BPM - random.uniform(1, 3))
            stat.pace = min(max_pace, stat.pace + random.uniform(0.1, 0.3))
        
        # Distance accumulée
        if stat.pace > 0:
            stat.distance += stat.pace * (1 / 3.6) * (stat.time - stats.first().time).total_seconds()

        # Ajustement des autres mesures de qualité et de risque
        stat.footing_quality = max(0.7, random.uniform(0.7, 0.95))  # Qualité de footing raisonnable
        stat.fatigue_level = min(1.0, stat.fatigue_level + 0.05)  # Légère augmentation de la fatigue
        stat.training_intensity = min(1.0, stat.training_intensity + 0.02)  # Intensité élevée après impact
        stat.concussion_risk = min(1.0, stat.concussion_risk + 0.03)  # Augmentation du risque de commotion

        # Sauvegarder la mise à jour
        stat.save()

    print(f"Mise à jour des données de session-stats pour la session ID {session_id} complétée avec succès.")



update_session_stats_for_impact(8)