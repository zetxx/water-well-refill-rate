const Koa = require('koa');
const Router = require('@koa/router');
const {listen, authorization, host, scheduler} = require('rc')(
    require('./package.json').name,
    {
        listen: 3000,
        authorization: '123',
        host: '123',
        scheduler: {type: 'static'}
    }
);
const {run} = require('./lib')({
    host,
    authorization,
    scheduler
});

const app = new Koa();
const router = new Router();

router.get('/water/:state/:rate', async(ctx, next) => {
    run(ctx);
    ctx.body = {};
});

app
    .use(router.routes())
    .use(router.allowedMethods());

console.info(`server listen on: ${listen}`);
console.info(`will send on host: ${host} authorization: ${authorization}`);
app.listen(listen);
