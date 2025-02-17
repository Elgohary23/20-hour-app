document.addEventListener('DOMContentLoaded', function() {
    const button = document.getElementById('demoButton');
    const result = document.getElementById('result');
    
    button.addEventListener('click', function() {
        result.textContent = 'Button clicked! JavaScript is working!';
        setTimeout(() => {
            result.textContent = '';
        }, 2000);
    });
});
