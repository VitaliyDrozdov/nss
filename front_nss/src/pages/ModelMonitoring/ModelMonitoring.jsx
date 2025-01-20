import React from "react";
import { useFormik } from "formik";
import {
  Box,
  Button,
  Checkbox,
  FormControlLabel,
  MenuItem,
  Select,
  TextField,
  Typography,
} from "@mui/material";
import api from "../../utils/api";

const ModelMonitoring = () => {

  const fetchData = async (values) => {
    try {
      const params = new URLSearchParams();

      if (values.model) params.append("model_name", values.model);
      if (values.metric) params.append("metric_name", values.metri);

      const response = await api.get(`/dwh/?${params.toString()}`);

      

      
      console.log(response.data.data);
    } catch (error) {
      console.error("Ошибка при загрузке данных:", error);
    }
  };


  const formik = useFormik({
    initialValues: {
      reportPeriod: "lastMonth",
      model: "model1",
      metric: "metric1",
      sendEmail: false,
      email: "",
    },
    onSubmit: (values) => {
      console.log("Form values:", values);
    },
  });

  




  return (
    <Box
      sx={{
        width: "600px",
        margin: "auto",
        marginTop: 8,
        padding: "20px",
        backgroundColor: "#1a2336",
        borderRadius: "10px",
        boxShadow: "0 4px 10px rgba(0,0,0,0.3)",
      }}
    >
      <Typography
        variant="h2"
        sx={{  marginBottom: "20px", textAlign: "center", fontWeight: "bold" }}
      >
        Введите данные для расчета
      </Typography>

      <form onSubmit={formik.handleSubmit}>
        
        <Box sx={{ marginBottom: "20px" }}>
          <Typography variant="h4" sx={{ color: "#fff", marginBottom: "5px" }}>
            Период отчета
          </Typography>
          <Select
            fullWidth
            id="reportPeriod"
            name="reportPeriod"
            value={formik.values.reportPeriod}
            onChange={formik.handleChange}
            sx={{
              backgroundColor: "#2e3b55",
              color: "#fff",
            }}
          >
            <MenuItem value="lastMonth">За последний месяц</MenuItem>
            <MenuItem value="lastWeek">За последнюю неделю</MenuItem>
          </Select>
        </Box>

        
        <Box sx={{ marginBottom: "20px" }}>
          <Typography variant="h4" sx={{ color: "#fff", marginBottom: "5px" }}>
            Модель
          </Typography>
          <Select
            fullWidth
            id="model"
            name="model"
            value={formik.values.model}
            onChange={formik.handleChange}
            sx={{
              backgroundColor: "#2e3b55",
              color: "#fff",
            }}
          >
            <MenuItem value="model1">Модель 1</MenuItem>
            <MenuItem value="model2">Модель 2</MenuItem>
          </Select>
        </Box>

        
        <Box sx={{ marginBottom: "20px" }}>
          <Typography variant="h4" sx={{ color: "#fff", marginBottom: "5px" }}>
            Метрика
          </Typography>
          <Select
            fullWidth
            id="metric"
            name="metric"
            value={formik.values.metric}
            onChange={formik.handleChange}
            sx={{
              backgroundColor: "#2e3b55",
              color: "#fff",
            }}
          >
            <MenuItem value="metric1">Метрика 1</MenuItem>
            <MenuItem value="metric2">Метрика 2</MenuItem>
          </Select>
        </Box>

        
        <Box sx={{ marginBottom: "20px" }}>
          <FormControlLabel
            control={
              <Checkbox
                id="sendEmail"
                name="sendEmail"
                checked={formik.values.sendEmail}
                onChange={formik.handleChange}
                color="secondary"
              />
            }
            label={
              <Typography sx={{ color: "#fff" }}>
                Отправить отчет на почту
              </Typography>
            }
          />
        </Box>

        
        {formik.values.sendEmail && (
          <Box sx={{ marginBottom: "20px" }}>
            <TextField
              fullWidth
              id="email"
              name="email"
              type="email"
              value={formik.values.email}
              onChange={formik.handleChange}
              placeholder="namepost@post.ru"
              sx={{
                backgroundColor: "#2e3b55",
                input: { color: "#fff" },
              }}
            />
          </Box>
        )}

        
        <Button
          fullWidth
          type="submit"
          variant="contained"
          color="secondary"
        >
          <Typography variant="h5">Сформировать отчет</Typography>
          
        </Button>
      </form>
    </Box>
  );
};


export default ModelMonitoring;