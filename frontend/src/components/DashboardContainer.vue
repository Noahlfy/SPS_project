<script setup>

const date = '09/10/2024';

const startSession = () => {
    console.log("Session should start")
}
</script>

<template>
    <section>
        <div class="dashboard-container">
            <div class="sessions">
                <div class="start">
                    <span class="text-2xl">Start a new session</span>
                    <button id="start-button" @click="startSession">
                        <RouterLink
                        to="/session"
                        > 
                        START
                        </RouterLink>
                    </button>
                </div>
                <div class="last-session-text">Last session - {{ date }}</div> 
                <div class="last-session">
                    
                    <ul>
                        <li>Productivity of last session :       INTENSE</li>
                        <li>Concussion risk : 30% </li>
                        <li>Days Of Rest Needed : 3 Days</li>
                    </ul>
                </div>
            </div>
            <div class="global-statistics">
                <div class="box" id="Concussion-passeport">
                    <div class="data-name">Concussion passeport</div>
                    <div class="data-value">5/10</div>
                </div>
                <div class="box" id="average-activity-during-sessions">
                    <div class="data-name">Average activity during sessions</div>
                    <div class="data-value">40%</div>
                </div>
                <div class="box" id="average-heart-rate">
                    <div class="data-name">Average heart rate</div>
                    <div class="data-value">67BPM</div>
                </div>
            </div>
        </div>
    </section>
</template>