import React, { useState } from "react";
import { useFormik } from "formik";
import {
  Box,
  Button,
  Checkbox,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControlLabel,
  MenuItem,
  Select,
  TextField,
  Typography,
} from "@mui/material";
import api from "../../utils/api";

const ModelMonitoring = () => {
  const [openDialog, setOpenDialog] = useState(false);
  const [fileUrl, setFileUrl] = useState("");

  const fetchData = async (values) => {
    try {
      const dataToSend = {
        model_name: values.model,
        metric_name: values.metric,
        monitoring_type: "On-demand",
        time_period: values.reportPeriod,
      };

      const response = await api.post(`/monitoring/create`, dataToSend);
      if (response.status === 201) {
        const fileResponse = await api.get(`/monitoring/download/${response.data.id}`, {
          responseType: "blob", // Получаем файл в формате blob
        });

        // Создаём URL для файла
        const url = window.URL.createObjectURL(new Blob([fileResponse.data]));
        setFileUrl(url); // Сохраняем URL для дальнейшего использования
        setOpenDialog(true); // Открываем диалог
      }
    } catch (error) {
      console.error("Ошибка при загрузке данных:", error);
    }
  };

  const handleDownload = () => {
    const link = document.createElement("a");
    link.href = fileUrl;
    link.setAttribute("download", "report.csv"); // Имя скачиваемого файла
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    setOpenDialog(false); // Закрываем диалог
  };

  const handleView = () => {
    window.open(fileUrl, "_blank"); // Открываем файл в новой вкладке
    setOpenDialog(false); // Закрываем диалог
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
      fetchData(values);
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
        sx={{ marginBottom: "20px", textAlign: "center", fontWeight: "bold" }}
      >
        Введите данные для расчета
      </Typography>

      <form onSubmit={formik.handleSubmit}>
        {/* Период отчета */}
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

        {/* Модель */}
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
            <MenuItem value="osago">ОСАГО</MenuItem>
            <MenuItem value="life">Страхование жизни</MenuItem>
          </Select>
        </Box>

        {/* Метрика */}
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
            <MenuItem value="Metric 1">Метрика 1</MenuItem>
            <MenuItem value="Metric 2">Метрика 2</MenuItem>
            <MenuItem value="Metric 3">Метрика 3</MenuItem>
          </Select>
        </Box>

        {/* Отправить на почту */}
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
                Отправить отчет на почту(разработка в процессе)
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

      {/* Диалог для выбора действия */}
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)}>
        <DialogTitle>Скачать или открыть отчет</DialogTitle>
        <DialogContent>
          <Typography>Выберите действие с отчетом:</Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleDownload} color="primary" variant="contained">
            Скачать
          </Button>
          <Button onClick={handleView} color="secondary" variant="outlined">
            Просмотреть
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default ModelMonitoring;
