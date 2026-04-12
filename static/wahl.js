document.addEventListener("DOMContentLoaded", function () {
    const rows = document.querySelectorAll("tr:has(input[type='radio'])");
    const listItems = document.querySelectorAll("ol li");

    // 👉 Merkt sich die letzte gültige Auswahl pro Gruppe
    const lastValidSelection = {};

    // 🔹 1. Initiale Auswahl setzen
    rows.forEach((row, rowIndex) => {
        const radios = row.querySelectorAll("input[type='radio']");

        radios.forEach((radio, colIndex) => {
            if (colIndex === rowIndex) {
                radio.checked = true;

                const projektName = row.querySelector("td a").textContent;
                listItems[colIndex].textContent = projektName;

                // speichern
                lastValidSelection[radio.name] = radio;
            }
        });
    });

    // 🔹 2. Event-Listener
    const allRadios = document.querySelectorAll("input[type='radio']");

    allRadios.forEach(radio => {
        radio.addEventListener("change", function () {
            const groupName = this.name;
            const index = parseInt(groupName.replace("wahl", "")) - 1;
            const selectedValue = this.value;

            // 👉 Prüfen, ob Projekt schon gewählt ist
            const alreadySelected = Array.from(document.querySelectorAll("input[type='radio']:checked"))
                .some(r => r !== this && r.value === selectedValue);

            if (alreadySelected) {
                // ❌ Auswahl verbieten → zurück zur alten
                if (lastValidSelection[groupName]) {
                    lastValidSelection[groupName].checked = true;
                }
                return;
            }

            // ✅ gültige Auswahl → speichern
            lastValidSelection[groupName] = this;

            // 👉 Liste aktualisieren
            const row = this.closest("tr");
            const projektName = row.querySelector("td a").textContent;
            listItems[index].textContent = projektName;
        });
    });
});
