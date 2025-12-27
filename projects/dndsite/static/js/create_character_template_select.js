// document.getElementById('selected_character_base').addEventListener('change', function() {
//     const selectedKey = this.value;
//     const nameField = document.getElementById('character_name');
//     const raceField = document.getElementById('race');

//     if (selectedKey && templates[selectedKey]) {
//         nameField.value = templates[selectedKey].subject;
//         raceField.value = templates[selectedKey].body;
//     } else {
//         nameField.value = '';
//         raceField.value = '';
//     }
// });

// Ждем полной загрузки DOM
document.addEventListener('DOMContentLoaded', function() {
    const dataSource = document.getElementById('templates-json');
    if (!dataSource) return;

    const templatesData = JSON.parse(dataSource.textContent);
    const selector = document.getElementById('selected_character_base');

    selector.addEventListener('change', function() {
        const selectedId = this.value;
        const data = templatesData[selectedId];

        if (data) {
            // Словарь соответствий: "ID в HTML": "Ключ в словаре Python"
            const mapping = {
                'character_name': 'character_name',
                'race': 'race',
                'class': 'character_class',        // Исправлено под ваш словарь
                'subclass': 'character_sub_class', // Исправлено под ваш словарь
                'strength': 'strength',
                'hit_points': 'max_hit_points',    // Исправлено под ваш словарь
                'armor_class': 'armor_class',
                'movement_speed': 'movement_speed',
                'aligment': 'alignment',
                'size': 'size',
                'age': 'age',
                'height': 'height',
                'weight': 'weight'
            };

            for (let [htmlId, apiKey] of Object.entries(mapping)) {
                const input = document.getElementById(htmlId);
                if (input) {
                    // Если значение null или undefined, ставим пустую строку/0
                    let val = data[apiKey];
                    input.value = (val !== null && val !== undefined) ? val : (input.type === 'number' ? 0 : "");
                }
            }
        }
    });
});