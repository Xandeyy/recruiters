import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Login = () => {
  const navigate = useNavigate(); // Get the history object from React Router
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/login/token/", {
        username: username,
        password: password,
      });

      // Assuming your backend returns a token upon successful login
      const token = response.data.access;

      // Store the token in local storage or a state management system (like Redux)
      localStorage.setItem("token", token);

      // Handle further actions, e.g., redirect to another page
      console.log("Login successful!");

      // Redirect to the home page or another route
      navigate("/login");
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handleLogin}>Loginn</button>
    </div>
  );
};

export default Login;
