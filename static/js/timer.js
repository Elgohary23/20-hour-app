document.addEventListener('DOMContentLoaded', function() {
    // Function to save durations to local storage
    function saveDurations(skillId, durations) {
        localStorage.setItem(`skill_${skillId}_durations`, JSON.stringify(durations));
    }

    // Function to retrieve durations from local storage
    function getDurations(skillId) {
        const durationsString = localStorage.getItem(`skill_${skillId}_durations`);
        return durationsString ? JSON.parse(durationsString) : [];
    }

    // Get the start button element
    const startButton = document.getElementById('startBtn');

    if (startButton) {
        startButton.addEventListener('click', function() {
            const skillId = document.querySelector('.skill-detail-container').dataset.skillId;
            const savedDurations = getDurations(skillId);
            const durationInput = document.getElementById('duration');
            const timerSection = document.querySelector('.timer-section');

            // Create the duration selection window
            const durationWindow = document.createElement('div');
            durationWindow.style.position = 'absolute';
            durationWindow.style.top = `${timerSection.offsetTop + timerSection.offsetHeight}px`;
            durationWindow.style.left = `${timerSection.offsetLeft}px`;
            durationWindow.style.zIndex = '1';
            durationWindow.style.border = '1px solid #ccc';
            durationWindow.style.background = '#fff';
            durationWindow.style.padding = '10px';

            // Display saved durations
            savedDurations.forEach(duration => {
                const durationItem = document.createElement('div');
                durationItem.textContent = `${duration} minutes`;
                durationItem.style.cursor = 'pointer';
                durationItem.addEventListener('click', function() {
                    // Set the timer duration input
                    durationInput.value = duration;
                    // Trigger the change event to update the timer display
                    durationInput.dispatchEvent(new Event('change'));
                    // Close the duration window
                    durationWindow.remove();
                });
                durationWindow.appendChild(durationItem);
            });

            // Add a "Custom" option
            const customOption = document.createElement('div');
            customOption.textContent = 'Custom';
            customOption.style.cursor = 'pointer';
            customOption.addEventListener('click', function() {
                // For now, just close the window - custom input is already available
                durationWindow.remove();
            });
            durationWindow.appendChild(customOption);

            document.body.appendChild(durationWindow);
        });
    }

    // Function to record duration (call this when a timer session ends)
    function recordDuration(skillId, duration) {
        let savedDurations = getDurations(skillId);
        savedDurations.push(duration);
        if (savedDurations.length > 3) {
            savedDurations.shift();
        }
        saveDurations(skillId, savedDurations);
    }

    // Add a data attribute to the skill detail container to store the skill ID
    const skillDetailContainer = document.querySelector('.skill-detail-container');
    if (skillDetailContainer) {
        const skillId = window.location.pathname.split('/').pop();
        skillDetailContainer.dataset.skillId = skillId;
    }
});
