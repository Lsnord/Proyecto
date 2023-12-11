// mascota.js
var RAZAS_PERRO = RAZAS_PERRO || [];
var RAZAS_GATO = RAZAS_GATO || [];

function actualizarRazas() {
    var tipoMascota = document.getElementById("id_tipos").value;
    var razasSelect = document.getElementById("id_raza");
    razasSelect.innerHTML = "";

    var razas;
    if (tipoMascota.toLowerCase() === "perro") {
        razas = RAZAS_PERRO;
    } else if (tipoMascota.toLowerCase() === "gato") {
        razas = RAZAS_GATO;
    }

    // Agrega las opciones de raza al campo de selección
    for (var i = 0; i < razas.length; i++) {
        var option = document.createElement("option");
        option.value = razas[i][0];
        option.text = razas[i][1];
        razasSelect.appendChild(option);
    }
}

document.getElementById("id_tipos").addEventListener("change", actualizarRazas);
// Mueve la llamada a actualizarRazas al final del archivo
window.onload = actualizarRazas;

