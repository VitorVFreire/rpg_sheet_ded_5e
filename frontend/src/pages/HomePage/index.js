import './HomePage.css'
import Banner from "../../components/Banner";
import Navbar from "../../components/Navbar";
import { useEffect } from 'react';

function HomePage(props) {
  const idUser = props.idUser; 
  useEffect(() => {
    document.title = 'Home';
  }, []);
  return (
    <div className="home">
      <Navbar isLoggedIn={idUser} /> 
      <Banner />
    </div>
  );
}

export default HomePage;