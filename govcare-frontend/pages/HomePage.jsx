import { Box, Typography, Card, CardContent } from "@mui/material";
import { useNavigate } from "react-router-dom";

const HomePage = () => {
  const navigate = useNavigate();

  return (
    <Box
      sx={{
        minHeight: "100vh",
        background: "linear-gradient(135deg, #0b102f, #020617)", // نفس الداشبورد
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      {/* السؤال */}
      <Typography
        variant="h4"
        sx={{
          color: "white",
          mb: 6,
          fontWeight: "bold",
          textAlign: "center",
        }}
      >
        هل أنت موظف أم مواطن؟
      </Typography>

      {/* الكروت */}
      <Box
        sx={{
          display: "flex",
          gap: 6,
          justifyContent: "center",
          flexWrap: "wrap",
        }}
      >
        {/* موظف */}
        <Card
          onClick={() => navigate("/login")}
          sx={{
            width: 260,
            height: 180,
            borderRadius: 4,
            cursor: "pointer",
            background: "linear-gradient(90deg, #7c3aed, #2563eb)",
            boxShadow: "0 8px 25px rgba(0,0,0,0.3)",
            transition: "0.3s",
            "&:hover": {
              transform: "translateY(-6px)",
              boxShadow: "0 15px 35px rgba(0,0,0,0.45)",
            },
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <CardContent>
            <Typography
              variant="h5"
              align="center"
              sx={{ fontWeight: "bold", color: "#0f172a" }}
            >
              موظف
            </Typography>
          </CardContent>
        </Card>

        {/* مواطن */}
        <Card
          onClick={() => navigate("/citizen")}
          sx={{
            width: 260,
            height: 180,
            borderRadius: 4,
            cursor: "pointer",
            background: "linear-gradient(90deg, #7c3aed, #2563eb)",
            boxShadow: "0 8px 25px rgba(0,0,0,0.3)",
            transition: "0.3s",
            "&:hover": {
              transform: "translateY(-6px)",
              boxShadow: "0 15px 35px rgba(0,0,0,0.45)",
            },
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <CardContent>
            <Typography
              variant="h5"
              align="center"
              sx={{ fontWeight: "bold", color: "#0f172a" }}
            >
              مواطن
            </Typography>
          </CardContent>
        </Card>
      </Box>
    </Box>
  );
};

export default HomePage;
