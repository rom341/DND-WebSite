import { stateReady } from './battle_state.js';

export async function renderBattleMap() {
    const battleState = await stateReady;
    const gridMap = document.getElementById("battle-map-grid");
    const cellTemplate = document.getElementById("battle-map-grid-cell-template");
    const characterMarkTemplate = document.getElementById("battle-map-character-mark-template");
    
    gridMap.style.display = 'grid';
    gridMap.style.width = '100%';
    gridMap.style.gridTemplateColumns = `repeat(${battleState.locationData.columns_count}, 50px)`;
    gridMap.innerHTML = '';
    console.log(battleState);
    for (let r = 0; r < battleState.locationData.rows_count; r++) {
        for (let c = 0; c < battleState.locationData.columns_count; c++) {            
            const gridCellFragment = cellTemplate.content.cloneNode(true);
            const gridCellInstance = gridCellFragment.querySelector('.battle-map-grid-cell');
            
            gridCellInstance.className = "grid-cell";
            gridCellInstance.dataset.x = c;
            gridCellInstance.dataset.y = r;

            const characterPositions = battleState.characterPositions.filter(p => p.column == c && p.row == r);
            if (characterPositions.length > 0) {
                characterPositions.forEach(characterPosition => {
                    const characterMarkFragment = characterMarkTemplate.content.cloneNode(true);
                    const characterMarkInstance = characterMarkFragment.querySelector('.character_mark');
                    if (characterMarkInstance != null) {
                        console.log("fd");
                        characterMarkInstance.textContent = characterPosition.character.character_name;
                        gridCellInstance.appendChild(characterMarkInstance);
                    }           
                });

            }
            gridMap.appendChild(gridCellInstance);
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    renderBattleMap();
});