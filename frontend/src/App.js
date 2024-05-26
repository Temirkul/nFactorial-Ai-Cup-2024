import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
    const [story, setStory] = useState([]);  // State now holds an array of story parts
    const [input, setInput] = useState('');
    const [chatVisible, setChatVisible] = useState(true);

    useEffect(() => {
        startStory();
        // You can set a default image or remove this if not using background images
        // setImage('path_to_default_background_image.jpg'); 
    }, []);

    const startStory = async () => {
        try {
            const response = await axios.post('http://localhost:8000/start-story');
            setStory([response.data.story_text]);  // Initialize story with the first part as an array
        } catch (error) {
            console.error('Failed to start story:', error.response ? error.response.data : error.message);
        }
    };

    const continueStory = async () => {
        if (!input.trim()) return; // Avoid adding empty inputs
        try {
            const response = await axios.post('http://localhost:8000/continue-story', {
                story_context: story.join("\n"),  // Join array elements with newline for the backend
                user_input: input
            });
            setStory(prevStory => [...prevStory, response.data.story_text]);  // Append new story part to array
            setInput('');
        } catch (error) {
            console.error('Failed to continue story:', error.response ? error.response.data : error.message);
        }
    };

    return (
        <div className="app">
            <div className="chat-window"
                onMouseEnter={() => setChatVisible(true)}
                onMouseLeave={() => setChatVisible(false)}
                style={{ opacity: chatVisible ? 1 : 0, transition: 'opacity 0.5s ease-in-out' }}>
                <div className="story-display">
                    {story.length === 0 ? "Loading story..." : story.map((paragraph, index) => (
                        <p key={index}>{paragraph}</p> // Render each story part as a separate paragraph
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
