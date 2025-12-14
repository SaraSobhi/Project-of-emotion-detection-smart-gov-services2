import { Box, Typography, TextField, Button, Card, Alert } from "@mui/material";
import { useState } from "react";

const CitizenPage = () => {
  const [complaint, setComplaint] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = () => {
    if (complaint.trim() === "") return;
    setSubmitted(true);
    setComplaint("");
  };

  return (
    <Box
      sx={{
        minHeight: "100vh",
        background: "linear-gradient(135deg, #0f172a, #020617)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        px: 2,
      }}
    >
      <Card
        sx={{
          width: "100%",
          maxWidth: 700,
          p: 5,
          background: "rgba(255,255,255,0.06)",
          backdropFilter: "blur(12px)",
          borderRadius: 4,
          boxShadow: "0 12px 32px rgba(0,0,0,0.4)",
          textAlign: "center",
        }}
      >
        <Typography
          variant="h4"
          sx={{ color: "#38bdf8", fontWeight: "bold", mb: 4 }}
        >
          أهلًا بك عزيزي المواطن
        </Typography>

        {/* رسالة التأكيد */}
        {submitted && (
          <Alert
            severity="success"
            sx={{
              mb: 3,
              background: "rgba(34,197,94,0.15)",
              color: "#22c55e",
              borderRadius: 2,
            }}
          >
            ✅ تم استلام الشكوى بنجاح
          </Alert>
        )}

        <TextField
          multiline
          rows={5}
          fullWidth
          placeholder="اكتب شكواك هنا..."
          variant="filled"
          value={complaint}
          onChange={(e) => setComplaint(e.target.value)}
          sx={{
            mb: 4,
            background: "rgba(255,255,255,0.08)",
            borderRadius: 2,
            textarea: {
              color: "white",
              fontSize: "16px",
            },
          }}
        />

        <Button
          size="large"
          onClick={handleSubmit}
          sx={{
            px: 5,
            py: 1.4,
            background: "linear-gradient(90deg, #38bdf8, #2563eb)",
            color: "white",
            fontSize: "16px",
            borderRadius: 3,
            "&:hover": { opacity: 0.9 },
          }}
        >
          إرسال الشكوى
        </Button>
      </Card>
    </Box>
  );
};

export default CitizenPage;
