
import AdminSidebar from "pages/AdminUsers/AdminSidebar";
import AdminTable from "pages/AdminUsers/AdminTable";
import TableSearchPage from "../wrapper/TableSearchPage";
import AdminTableSearchPage from "../wrapper/AdminTableSearchPage";

export default function Admin() {
  return (
    <AdminTableSearchPage
      SidebarComponent={AdminSidebar}
      TableComponent={AdminTable}
      apiName="users"
      label="usuarios"
    />
  );
}