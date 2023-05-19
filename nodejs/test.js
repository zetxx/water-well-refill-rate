const {run} = require('./lib')({
    host: 'eo6t8uxszs45p74.m.pipedream.net',
    authorization: 123,
    scheduler: {type: 'proportional'}
});
const timer = ({state, wait = 2}) => new Promise(
    (resolve, reject) => setTimeout(
        () => resolve(
            run({params: {state: String(state), rate: '0'}})
        ),
        wait * 500
    )
);

(async() => {
    await timer({state: 2});
    await timer({state: 1});
    await timer({state: 0});
    await timer({state: 1});
    await timer({state: 0});
})();
