const http = require('http');
const schedulers = require('./schedulers');

const Rq = ({host, authorization}) => (turn) => {
    const url = `http://${host}/relay/0?turn=${turn}`;
    console.info(url);
    const r = http.get(
        url,
        {headers: {Authorization: authorization}},
        (res) => {
            const {statusCode} = res;
            if (statusCode !== 200) {
                console.error(`HTTP Error: ${statusCode}`);
            }
        }
    );
    r.on('error', (e) => console.error(e.message));
};

const Run = ({
    pumpOff,
    pumpOn,
    scheduler
}) => {
    let z = 0;
    let dtn = 0;
    let safeOff = null;
    let onAfter = null;
    let controllerAwake = 0;
    let lastNoWater = 0;

    return ({params: {state, rate}}) => {
        console.log({
            z,
            dtn,
            onAfter: (onAfter !== null),
            safeOff: (safeOff !== null),
            controllerAwake,
            lastNoWater
        });
        setTimeout(() => {
            if (state === '1') { // water detected
                console.log('Water flows');
                if (lastNoWater && Math.floor((Date.now() - lastNoWater) / 1000) <= 10) {
                    return console.error('Off On flapping detected');
                }
                if (dtn) {
                    return console.error('Start time is not zero! state mismatch');
                }
                dtn = Date.now();
            } else if (state === '2') { // ping
                console.log('Online ping');
                controllerAwake = 1;
            } else if (state === '0') { // water NOT detected
                lastNoWater = Date.now();
                const ranFor = Math.floor((Date.now() - dtn) / 1000);
                console.log('water NOT detected');
                pumpOff();
                clearInterval(safeOff);
                controllerAwake = 0;
                if (dtn === 0) {
                    return console.error('Start time is zero! state mismatch');
                }
                if (onAfter !== null) {
                    dtn = 0;
                    return console.error('Pump on schedule already started');
                }
                const rfc = scheduler({
                    currentRun: ranFor,
                    z: ++z
                });
                dtn = 0;
                onAfter = setTimeout(() => {
                    pumpOn();
                    safeOff = setInterval(() => {
                        if (!controllerAwake) {
                            pumpOff();
                            clearInterval(safeOff);
                        }
                        controllerAwake = 0;
                    }, 10000);
                    onAfter = null;
                }, rfc.runAfter * 1000);
                console.log(rfc, {rate});
            }
        }, 10);
    };
};

module.exports = ({host, authorization, scheduler}) => {
    const rq = Rq({host, authorization});
    const pumpOff = () => rq('off');
    const pumpOn = () => rq('on');

    const schedulerRdy = Object.keys(schedulers).reduce(
        (ss, sc) => ({
            ...ss,
            [sc.toLowerCase()]: schedulers[sc](scheduler)
        }),
        {}
    );

    return {
        pumpOff,
        pumpOn,
        run: Run({
            pumpOff,
            pumpOn,
            scheduler: schedulerRdy[scheduler.type]
        })
    };
};
