import React, { useState } from "react";
import { Box, Grid, Card, CardContent, Typography, Switch, Button } from "@mui/material";
import Header from "../../components/Header";

const ModelCatalog = () => {
    const [models, setModels] = useState([
        { id: 1, name: "Название модели 1", status: false },
        { id: 2, name: "Название модели 2", status: true },
        { id: 3, name: "Название модели 3", status: true },
        { id: 4, name: "Название модели 4", status: false },
        { id: 5, name: "Название модели 5", status: false },
        { id: 6, name: "Название модели 6", status: false },
    ]);

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

    const handleToggle = (id) => {
        setModels((prevModels) =>
            prevModels.map((model) =>
                model.id === id ? { ...model, status: !model.status } : model
            )
        );
    };

    return (
        <>
            <Header title="Каталог моделей" sx={{marginLeft: 3}}/>



            <Box sx={{ padding: 3, backgroundColor: "#1A202C", minHeight: "100vh", color: "#fff" }}>
                <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 3 }}>
                    <Button variant="contained" sx={{ backgroundColor: "#7e6fd3" }}>
                        Добавить новую модель
                    </Button>
                </Box>
                <Grid container spacing={2}>
                    {models.map((model) => (
                        <Grid item xs={12} sm={6} md={4} key={model.id}>
                            <Card sx={{ backgroundColor: "#2D3748", color: "#fff" }}>
                                <CardContent>
                                    <Typography variant="h4">{model.name}</Typography>
                                    <Typography variant="body2" color="textSecondary" sx={{ marginBottom: 2 }}>
                                        Продукт
                                    </Typography>
                                    <Typography variant="h5" sx={{ marginBottom: 2 }}>
                                        {model.status ? "Включена" : "Отключена"}
                                    </Typography>
                                    <Switch
                                        checked={model.status}
                                        sx={SwitchStyle}
                                        onChange={() => handleToggle(model.id)}
                                    />
                                </CardContent>
                            </Card>
                        </Grid>
                    ))}
                </Grid>
            </Box>
        </>
    );
};

export default ModelCatalog;
