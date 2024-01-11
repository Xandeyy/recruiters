const Navbar = () => {
  return (
    <nav className="bg-green-600 p-2">
      <div className="container mx-auto flex item-center justify-between">
        <div className="text-white font-bold text-xl p-1">LOGO</div>

        <div className="flex space-x-4 ">
          <a
            href="/home"
            className="text-white p-2 hover:bg-blue-800 rounded-xl"
          >
            HOME
          </a>
          <a href="#" className="text-white p-2 hover:bg-blue-800 rounded-xl">
            ABOUT
          </a>
          <a href="#" className="text-white p-2 hover:bg-blue-800 rounded-xl">
            MENU
          </a>
          <a href="#" className="text-white p-2 hover:bg-blue-800 rounded-xl">
            RESERVATION
          </a>
          <a href="#" className="text-white p-2 hover:bg-blue-800 rounded-xl">
            CONTACT
          </a>
          <a href="#" className="text-white bg-gray-800 rounded-xl p-2">
            LOGIN
          </a>
          <a href="#" className="text-white bg-gray-800 rounded-xl p-2">
            SIGNUP
          </a>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
