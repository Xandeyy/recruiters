import Navbar from "./Navbar";

const Layout = ({ children }) => {
  return (
    <div>
      <Navbar />
      {children}
      {/* <div>footer</div> */}
    </div>
  );
};

export default Layout;
