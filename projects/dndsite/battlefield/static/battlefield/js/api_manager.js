export class APIManager {
    constructor() {
        this.baseBattlefieldUrl = '/battlefield';
        this.baseLobbyUrl = '/lobby';        
        this.baseCharacterUrl = '/characters';
    }

    async getCharacterPositions(locationId) {
        try {
            const response = await fetch(`${this.baseBattlefieldUrl}/get_character_positions_in_location/${locationId}/`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error("Failed to fetch positions:", error);
            return [];
        }
    }

    async getLocation(locationId) {
        try {
            const response = await fetch(`${this.baseBattlefieldUrl}/get_location/${locationId}/`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error("Failed to fetch location data:", error);
            return [];
        }
    }
    
    async getLocationsForLobby(lobbyId) {
        try {
            const response = await fetch(`${this.baseLobbyUrl}/get_locations_for_lobby/${lobbyId}/`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error("Failed to fetch locations for lobby data:", error);
            return [];
        }
    }

    async getLobby(lobbyId) {
        try {
            const response = await fetch(`${this.baseLobbyUrl}/get_lobby/${lobbyId}/`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error("Failed to fetch lobby data:", error);
            return [];
        }
    }

    async createLocation(data) {
        try {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const response = await fetch(`${this.baseBattlefieldUrl}/create_location_api/`, {
                method: "POST",
                body: JSON.stringify(data),
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken
                }
            });

            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error("Failed to fetch lobby data:", error);
            return [];
        }
    }
}