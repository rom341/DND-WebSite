document.addEventListener('DOMContentLoaded', function() {
    const dataSource = document.getElementById('templates-json');
    if (!dataSource) return;

    const templatesData = JSON.parse(dataSource.textContent);
    const selector = document.getElementById('selected_character_base');

    selector.addEventListener('change', function() {
        const selectedId = this.value;
        const data = templatesData[selectedId];
        if (data) {
            for (let [htmlId, apiKey] of Object.entries(data)) {
                const input = document.getElementById(htmlId);
                if (input) {
                    let val = apiKey;
                    input.value = (val !== null && val !== undefined) ? val : (input.type === 'number' ? 0 : "");
                }
            }
        }
    });
});