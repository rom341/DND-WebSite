export class BattlefieldAPI {
    constructor(baseUrl = '/battlefield') {
        this.BASE_URL = baseUrl;
    }

    async getCharacterPositions(lobbyId) {
        try {
            const response = await fetch(`${this.BASE_URL}/character_position_in_location/${lobbyId}/`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error("Failed to fetch positions:", error);
            return [];
        }
    }
}