import NavBar from "components/navbar/NavBar";
import React from "react";
import { Outlet } from "react-router-dom";

export default function NavBarRouterPage() {
  return (
    <React.Fragment>
      <NavBar />
      <Outlet />
    </React.Fragment>
  );
}
