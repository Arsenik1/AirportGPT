interface ChatResponse {
	reply: string;
}

export const sendChatMessage = async (message: string): Promise<ChatResponse> => {
	const response = await fetch('http://localhost:8002/chat', {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ message }),
	});

	// console.log(JSON.stringify({ message }));

	if (!response.ok) {
		throw new Error('Network response was not ok');
	}

	return response.json();
};

export const clearChatContext = async (): Promise<{ cleared: boolean }> => {
	const response = await fetch('http://localhost:8002/chat', {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ message: 'CLEAR_CONTEXT' }),
	});

	if (!response.ok) {
		throw new Error('Network response was not ok');
	}

	const data = await response.json();
	return { cleared: data.reply?.toLowerCase().includes('context cleared') ?? false };
};
