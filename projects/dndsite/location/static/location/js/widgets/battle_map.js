import { stateReady } from '../../../battlefield/js/battle_state.js';

export async function renderBattleMap() {
    const battleState = await stateReady;
    const gridMap = document.getElementById("battle-map-grid");
    const cellTemplate = document.getElementById("battle-map-grid-cell-template");
    const characterMarkTemplate = document.getElementById("battle-map-character-mark-template");
    
    gridMap.style.display = 'grid';
    gridMap.style.width = '100%';
    gridMap.style.gridTemplateColumns = `repeat(${battleState.selectedLocationData.columnsCount}, 50px)`;
    gridMap.innerHTML = '';
    for (let r = 0; r < battleState.selectedLocationData.rowsCount; r++) {
        for (let c = 0; c < battleState.selectedLocationData.columnsCount; c++) {      
            const gridCellFragment = cellTemplate.content.cloneNode(true);
            const gridCellInstance = gridCellFragment.querySelector('.battle-map-grid-cell');
            
            gridCellInstance.className = "grid-cell";
            gridCellInstance.dataset.x = c;
            gridCellInstance.dataset.y = r;

            const characterPositions = battleState.selectedLocationData.characterPositions.filter(p => p.column == c && p.row == r);
            if (characterPositions.length > 0) {
                characterPositions.forEach(characterPosition => {
                    const characterMarkFragment = characterMarkTemplate.content.cloneNode(true);
                    const characterMarkInstance = characterMarkFragment.querySelector('.character_mark');
                    if (characterMarkInstance != null) {
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