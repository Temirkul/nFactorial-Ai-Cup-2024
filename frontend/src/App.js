import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
    const [story, setStory] = useState([]);
    const [input, setInput] = useState('');
    const [image, setImage] = useState('');
    const [chatVisible, setChatVisible] = useState(true);

    useEffect(() => {
        startStory();
    }, []);

    const startStory = async () => {
        try {
            const response = await axios.post('http://localhost:8000/start-story');
            setStory([response.data.story_text]);
            updateImage(response.data.story_text);  // Initiate image update with initial story text
        } catch (error) {
            console.error('Failed to start story:', error.response ? error.response.data : error.message);
        }
    };

    const continueStory = async () => {
        if (!input.trim()) return;
        try {
            const response = await axios.post('http://localhost:8000/continue-story', {
                story_context: story.join("\n"),
                user_input: input
            });
            setStory(prevStory => [...prevStory, response.data.story_text]);
            updateImage(response.data.story_text);  // Update image with the new story segment
            setInput('');
        } catch (error) {
            console.error('Failed to continue story:', error.response ? error.response.data : error.message);
        }
    };

    // Function to fetch and update the image based on the story text
    const updateImage = async (storyText) => {
        try {
            const response = await axios.get(`http://localhost:8000/generate-image-pipeline`, {
                params: { story_at_current_timestep: storyText },
                responseType: 'blob'  // Important: Handle the response as a Blob
            });
            const imageUrl = URL.createObjectURL(response.data);  // Create a URL from the Blob
            setImage(imageUrl);  // Update state to reflect the new image URL
        } catch (error) {
            console.error('Failed to generate image:', error);
        }
    };

    return (
        <div className="app" style={{ backgroundImage: `url(${image})` }}>
            <div className="chat-window"
                onMouseEnter={() => setChatVisible(true)}
                onMouseLeave={() => setChatVisible(false)}
                style={{ opacity: chatVisible ? 1 : 0, transition: 'opacity 0.5s ease-in-out' }}>
                <div className="story-display">
                    {story.length === 0 ? "Loading story..." : story.map((paragraph, index) => (
                        <p key={index}>{paragraph}</p>
                    ))}
                </div>
                <textarea
                    value={input}
                    onChange={e => setInput(e.target.value)}
                    className="story-input"
                    placeholder="Continue the story..."
                />
                <button onClick={continueStory}>Send</button>
            </div>
        </div>
    );
}

export default App;
