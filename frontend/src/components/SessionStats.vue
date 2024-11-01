<script setup>

const playButton = 'Start';
const stopButton = 'Stop';

const isActive = true;
const sessionName = "Session 1"
</script>

<template>
    <section>
        <div class="stats-container">
            <div class="buttons-display">
                <div class="buttons">
                    <button type="submit" class="play">
                        {{ playButton }}
                    </button>
                    <button type="submit" class="stop">
                        {{ stopButton }}
                    </button>
                </div>
                <div class="session-name">
                    <div v-if="isActive">
                        {{ sessionName }}
                    </div>
                    <div v-else>
                        <input type="text" v-model="sessionName" placeholder="Session Name" />
                    </div>
                </div>
            </div>
            <div class="player-stats">
                <div class="stats" id="distance">
                    <div class="stats-name">Distance</div>
                    <div class="stats-data">2.5km</div>
                </div>
                <div class="stats" id="fatigue-level">
                    <div class="stats-name">Fatigue Level</div>
                    <div class="stats-data">20%</div>
                </div>
                <div class="stats" id="position-quality">
                    <div class="stats-name">Position quality</div>
                    <div class="stats-data">90%</div>
                </div>
                <div class="stats" id="training-intensity">
                    <div class="stats-name">Training intensity</div>
                    <div class="stats-data">90%</div>
                </div>
                <div class="stats" id="concussion-risk">
                    <div class="stats-name">Concussion risk</div>
                    <div class="stats-data">3/5</div>
                </div>
            </div>
        </div>
    </section>
</template>