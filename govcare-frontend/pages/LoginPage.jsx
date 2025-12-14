import { Box, Card, TextField, Typography, Button } from "@mui/material";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const navigate = useNavigate();

  const handleLogin = () => {
    // مؤقتًا من غير باك
    navigate("/dashboard");
  };

  return (
    <Box
      sx={{
        minHeight: "100vh",
        background: "linear-gradient(135deg, #1e1b4b, #020617)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <Card
        sx={{
          width: 380,
          padding: 4,
          background: "rgba(255,255,255,0.08)",
          backdropFilter: "blur(12px)",
          borderRadius: 4,
          color: "white",
        }}
      >
        <Typography variant="h4" align="center" gutterBottom>
          SIGN IN
        </Typography>

        <Typography
          variant="body2"
          align="center"
          sx={{ opacity: 0.8, mb: 3 }}
        >
          Sign in with your email
        </Typography>

        <TextField
          fullWidth
          label="Email"
          variant="filled"
          sx={{ mb: 2, input: { color: "white" } }}
        />

        <TextField
          fullWidth
          type="password"
          label="Password"
          variant="filled"
          sx={{ mb: 3, input: { color: "white" } }}
        />

        <Button
          fullWidth
          size="large"
          onClick={handleLogin}
          sx={{
            background: "linear-gradient(90deg, #7c3aed, #2563eb)",
            color: "white",
            py: 1.2,
            borderRadius: 3,
          }}
        >
          Sign In
        </Button>
      </Card>
    </Box>
  );
};

export default Login;
