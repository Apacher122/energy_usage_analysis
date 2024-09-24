import routes from './routes/routes.js';
import { socketApi } from './socket/socket_handler.js';
import express  from 'express';
import path from 'path';
import { createServer } from 'http';
import { fileURLToPath } from 'url';


const app = express();
    app.use(routes);
    app.use(express.json());
    app.use(express.static("./web_pages/"));
const httpServer = createServer(app);

const __filename = fileURLToPath(import.meta.url); // get the resolved path to the file
const __dirname = path.dirname(__filename); // get the name of the director

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname,'./web_pages/index.html'))
});

const port = process.env.PORT | 4103;
httpServer.listen(port)

socketApi.io.attach(httpServer);