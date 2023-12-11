document.addEventListener('DOMContentLoaded', function () {
    var historialBtn = document.getElementById('historialBtn');
    var historialDiv = document.getElementById('historialDiv');

    historialBtn.addEventListener('click', function () {
        historialDiv.style.display = 'block';
    });
});