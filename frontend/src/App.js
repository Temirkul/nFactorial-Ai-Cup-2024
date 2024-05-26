import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
    const [story, setStory] = useState('');  // Stores the entire story text
    const [input, setInput] = useState('');  // User input for continuing the story
    const [image, setImage] = useState(null); // For background image
    const [chatVisible, setChatVisible] = useState(true); // Controls chat window visibility

    useEffect(() => {
        startStory();
        // You can set a default image or remove this if not using background images
        // setImage('path_to_default_background_image.jpg'); 
    }, []);

    const startStory = async () => {
        try {
            const response = await axios.post('http://localhost:8000/start-story');
            setStory(response.data.story_text);
            console.log("Initial story fetched:", response.data.story_text);
        } catch (error) {
            console.error('Failed to start story:', error.response ? error.response.data : error.message);
        }
    };

    const continueStory = async () => {
        if (!input.trim()) return;
        try {
            const response = await axios.post('http://localhost:8000/continue-story', {
                story_context: story,
                user_input: input
            });
            setStory(prev => prev + "\n" + response.data.story_text);
            setInput('');
            console.log("Story continued:", response.data.story_text);
        } catch (error) {
            console.error('Failed to continue story:', error.response ? error.response.data : error.message);
        }
    };

    return (
        <div className="app" style={{ backgroundImage: `url(${image})` }}>
            <div className="story-display">
                {story || "Loading story..."}
            </div>
            <div className="chat-interface"
                onMouseEnter={() => setChatVisible(true)}
                onMouseLeave={() => setChatVisible(false)}
                style={{ opacity: chatVisible ? 1 : 0, transition: 'opacity 0.5s' }}>
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
