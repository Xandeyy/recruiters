import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Login from "./components/Login";
import Layout from "./components/Layout";

function App() {
  return (
    <Layout>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          {/* Add more routes as needed */}
        </Routes>
      </Router>
    </Layout>
  );
}

export default App;
