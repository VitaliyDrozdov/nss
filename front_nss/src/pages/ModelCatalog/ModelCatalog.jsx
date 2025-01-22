import React, { useState } from "react";
import { Box, Grid, Card, CardContent, Typography, Switch, Button, Dialog, DialogActions, DialogContent, DialogTitle, MenuItem, Select, TextField, FormControlLabel } from "@mui/material";
import Header from "../../components/Header";
import api from "../../utils/api";


const ModelCatalog = () => {
    const [models, setModels] = useState([]);
    const [formData, setFormData] = useState({
        model_name: "",
        product_code: "",
        status: false,
        model_version: "1.0",
        model_description: ""
    });

    const [open, setOpen] = useState(false);

    const handleChange = (field, value) => {
        setFormData((prev) => ({ ...prev, [field]: value }));
    };

    const handleOpenDialog = () => {
        setOpen(true);
    };

    const handleCloseDialog = () => {
        setOpen(false);
    };

    const getModels = async () => {
        const params = new URLSearchParams();
        params.append("page", 1);
        params.append("per_page", 10);
        const response = await api.get(`/model_catalog/?${params.toString()}`);
        setModels(response.data.data);
        console.log(models);
    };

    const SwitchStyle = {
        width: 80,
        height: 40,
        padding: 0,
        marginRight: 40,

        '& .MuiSwitch-switchBase': {
            padding: 0,
            marginTop: 'auto',
            marginBottom: 'auto',

            '&.Mui-checked': {
                transform: 'translateX(40px)',
                color: '#7e6fd3',
            },
        },
        '& .MuiSwitch-thumb': {
            width: 40,
            height: 40,
        },
        '& .MuiSwitch-track': {
            borderRadius: 15,
            backgroundColor: '#acaed1',

        },
        '& .Mui-checked + .MuiSwitch-track': {
            backgroundColor: '#acaed1',
        }
    };

    const handleToggle = async (name) => {
        const updatedModels = models.map((model) =>
            model.model_name === name ? { ...model, status: !model.status } : model
        );
    
        const updatedModel = updatedModels.find((model) => model.model_name === name);
    
        try {
            await api.put(`/model_catalog/${updatedModel.model_name}`, {
                status: updatedModel.status,
            });
    
            setModels(updatedModels);
        } catch (error) {
            console.error("Ошибка при обновлении статуса модели:", error);
        }
    };

    const handleCreation = async () => {
        try {

            const dataToSend = {
                model_name: formData.model_name,
                product_code: "prod002",
                status: false,
                model_version: "1.0",
                model_description: formData.model_description

            };


            const response = await api.post("/model_catalog/", dataToSend);
            console.log("Успешное создание модели:", response.data);


            setFormData({
                model_name: "",
                product_code: "",
                status: false,
                model_version: "1.0",
                model_description: ""
            });
            getModels();

            handleCloseDialog();
        } catch (error) {
            console.error("Ошибка при создании инцидента:", error);
        }
    };

    React.useEffect(() => {
        getModels();
    }, []);

    return (
        <>
            <Header title="Каталог моделей" sx={{ marginLeft: 3 }} />
            <Box sx={{ padding: 3, backgroundColor: "#1A202C", minHeight: "100vh", color: "#fff" }}>
                <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 3 }}>
                    <Button variant="contained" sx={{ backgroundColor: "#7e6fd3" }} onClick={handleOpenDialog}>
                        Добавить новую модель
                    </Button>
                </Box>
                <Grid container spacing={2}>
                    {models.map((model) => (
                        <Grid item xs={12} sm={6} md={4} key={model.id}>
                            <Card sx={{ backgroundColor: "#2D3748", color: "#fff" }}>
                                <CardContent>
                                    <Typography variant="h4">{model.model_name}</Typography>
                                    <Typography variant="body2" color="textSecondary" sx={{ marginBottom: 2 }}>
                                        Продукт
                                    </Typography>
                                    <Typography variant="h5" sx={{ marginBottom: 2 }}>
                                        {model.status ? "Включена" : "Отключена"}
                                    </Typography>
                                    <Switch
                                        checked={model.status}
                                        sx={SwitchStyle}
                                        onChange={() => handleToggle(model.model_name)}
                                    />
                                </CardContent>
                            </Card>
                        </Grid>
                    ))}
                </Grid>
            </Box>

            {/* Модальное окно */}
            <Dialog open={open} onClose={handleCloseDialog} fullWidth maxWidth="md" >
                <DialogTitle><Typography variant="h3">Добавление новой модели</Typography></DialogTitle>
                <DialogContent>
                    <Box display="grid" gap={2}>
                        <Box display="flex">
                            <Box width={400} height={53} bgcolor="#2b2b3d" p={2}>
                                <Typography variant="h5" sx={{ color: "#fff", marginBottom: 1 }}>
                                    Название модели
                                </Typography>
                            </Box>
                            <TextField
                                fullWidth
                                multiline
                                rows={1}
                                value={formData.model_name}
                                onChange={(e) => handleChange("model_name", e.target.value)}
                            />

                        </Box>
                        <Box display="flex">
                            <Box width={400} height={53} bgcolor="#2b2b3d" p={2}>
                                <Typography variant="h5" sx={{ color: "#fff", marginBottom: 1 }}>
                                    Тип продукта
                                </Typography>

                            </Box>
                            <Select
                                fullWidth
                                value={formData.product_code}
                                onChange={(e) => handleChange("product_code", e.target.value)}
                            >
                                <MenuItem value="OSAGO">ОСАГО</MenuItem>
                                <MenuItem value="LIFE">Страхование жизни</MenuItem>
                            </Select>
                        </Box>
                        <Box display="flex">
                            <Box width={400} bgcolor="#2b2b3d" p={2}>
                                <Typography variant="h5" sx={{ color: "#fff", marginBottom: 1 }}>
                                    Описание модели
                                </Typography>
                            </Box>
                            <TextField
                                fullWidth
                                multiline
                                rows={3}
                                value={formData.model_description}
                                onChange={(e) => handleChange("model_description", e.target.value)}
                            />
                        </Box>
                    </Box>
                </DialogContent>
                <Box
                    display="flex"
                    justifyContent="space-between"
                    alignItems="center"
                    px={3}
                    py={1}
                    bgcolor="#2b2b3d"
                >

                    <DialogActions>
                        <Button onClick={handleCloseDialog} color="third">
                            Отмена
                        </Button>
                        <Button onClick={handleCreation} color="secondary" variant="contained">
                            Создать модель
                        </Button>
                    </DialogActions>
                </Box>
            </Dialog>
        </>
    );
};

export default ModelCatalog;
