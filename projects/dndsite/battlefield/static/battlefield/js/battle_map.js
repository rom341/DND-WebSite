import { stateReady } from './battle_state.js';

export async function renderBattleMap() {
    const battleState = await stateReady;
    const gridMap = document.getElementById("battle-map-grid");
    const cellTemplate = document.getElementById("battle-map-grid-cell-template");
    
    gridMap.style.display = 'grid';
    gridMap.style.width = '100%';
    gridMap.style.gridTemplateColumns = `repeat(${battleState.locationData.columns_count}, 50px)`;
    gridMap.innerHTML = '';
    for (let r = 0; r < battleState.locationData.rows_count; r++) {
        for (let c = 0; c < battleState.locationData.columns_count; c++) {            
            const fragment = cellTemplate.content.cloneNode(true);
            const cellInstance = fragment.querySelector('.battle-map-grid-cell');
            
            cellInstance.className = "grid-cell";
            cellInstance.dataset.x = c;
            cellInstance.dataset.y = r;

            const characterPosition = battleState.characterPositions.find(p => p.column == c && p.row == r);  

            if (characterPosition) {
                const mark = cellInstance.querySelector('.character_mark');
                mark.textContent = characterPosition.character.character_name;
            } else {
                cellInstance.querySelector('.character_mark').remove();
            }

            gridMap.appendChild(cellInstance);
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    renderBattleMap();
});