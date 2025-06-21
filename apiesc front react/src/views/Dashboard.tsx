import { useNavigate } from "react-router-dom";

function Dashboard() {
 const navigate = useNavigate();
 const userLs =localStorage.getItem("user");
const user = JSON.parse(userLs || "{}")
const firstname = user.firstname
const type = user.type
const lastname = user.lastname
const dni = user.dni
console.log(user) 

function logout (){
 localStorage.removeItem("user")
localStorage.removeItem("token")
 navigate("/login")
  }


      


 return (
    <div style={dashboardContainerStyle}>
     
        <div style={welcomeTextStyle}>
          Bienvenido {type} {firstname}
        </div>

        <div style={dividerStyle}></div>

        <div style={infoTextStyle}>Tu apellido es: {lastname}</div>
        <div style={infoTextStyle}>Tu DNI es: {dni}</div>

        <button
          style={
            buttonStyle
          }
  
          onClick={logout}
        >
          Cerrar sesión
        </button>
  
    </div>
  );
};

const dashboardContainerStyle: React.CSSProperties = {
  minHeight: "100vh",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  backgroundColor: "#121212",
  fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
  padding: "1rem",
};

const welcomeTextStyle: React.CSSProperties = {
  fontSize: "1.5rem",
  fontWeight: "600",
  marginBottom: "1rem",
  color: "#ffffff",
};

const dividerStyle: React.CSSProperties = {
  height: "1px",
  backgroundColor: "#444",
  margin: "1rem 0",
};

const infoTextStyle: React.CSSProperties = {
  fontSize: "1rem",
  marginBottom: "0.75rem",
  color: "#cccccc",
};

const buttonStyle: React.CSSProperties = {
  backgroundColor: "#4f9ded",
  borderColor: "#4f9ded",
  color: "#ffffff",
  fontWeight: "600",
  padding: "0.75rem 1.5rem",
  borderRadius: "6px",
  fontSize: "1rem",
  transition: "background-color 0.3s ease, transform 0.2s ease",
  cursor: "pointer",
  marginTop: "1.5rem",
};


export default Dashboard