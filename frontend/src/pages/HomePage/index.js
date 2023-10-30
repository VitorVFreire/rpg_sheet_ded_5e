import './HomePage.css'
import Banner from "../../components/Banner";
import Navbar from "../../components/Navbar";

function HomePage() {
  return (
    <div className="home">
      <Navbar />
      <Banner />
    </div>
  );
}

export default HomePage;