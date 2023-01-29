import {Route, Navigate} from "react-router-dom";
import { useContext } from "react";
import AuthContext from "contexts/UserContext";

function PrivateRoute({children, ...rest}){
    let { user } = useContext(AuthContext);
    let { permissions } = useContext(AuthContext);
    if(!user) {
        return <Navigate to="/login" />;
    }
    const [isSportCoordinator, isEventCoordinator, isUniversityCoordinator, isTeamCoordinator, admin] = Object.entries(permissions);
    const authorizate = (isSportCoordinator || isEventCoordinator || isUniversityCoordinator || isTeamCoordinator || admin);
    return !authorizate ? <Navigate to="/login" /> : children};


export default PrivateRoute;