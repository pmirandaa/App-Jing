import NavBar from "components/navbar/NavBar";
import styles from "./App.module.css";
import { Outlet } from "react-router-dom";

function App() {
  return (
    <div className={styles.root}>
      <NavBar/>
      <Outlet/>
    </div>
  );
}

export default App;
