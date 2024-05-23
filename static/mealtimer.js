        const mealTimesWeekday = [
            { start: "08:00", end: "09:15" },
            { start: "11:30", end: "14:00" },
            { start: "17:00", end: "19:00" }
        ];

        const mealTimesWeekend = [
            { start: "09:00", end: "10:00" },
            { start: "12:00", end: "13:30" },
            { start: "17:00", end: "19:00" }
        ];

        function getMealTimes() {
            const now = new Date();
            const day = now.getDay();
            return (day === 0 || day === 6) ? mealTimesWeekend : mealTimesWeekday;
        }

        function timeStringToDate(timeString) {
            const now = new Date();
            const [hours, minutes] = timeString.split(":").map(Number);
            return new Date(now.getFullYear(), now.getMonth(), now.getDate(), hours, minutes);
        }

        function updateTimer() {
            const now = new Date();
            const mealTimes = getMealTimes();
            let nextMeal = null;
            let message = "";

            for (const mealTime of mealTimes) {
                const start = timeStringToDate(mealTime.start);
                const end = timeStringToDate(mealTime.end);

                if (now >= start && now <= end) {
                    message = "Şu an yemek zamanı!";
                    break;
                } else if (now < start) {
                    nextMeal = start;
                    break;
                }
            }

            if (!message) {
                if (nextMeal) {
                    const diff = nextMeal - now;
                    const hours = Math.floor(diff / 1000 / 60 / 60);
                    const minutes = Math.floor((diff / 1000 / 60) % 60);
                    if (hours > 0) {
                        message = `Bir sonraki yemek <strong>${hours} saat ${minutes} dakika</strong> sonra.`;
                    } else {
                        message = `Bir sonraki yemek <strong>${minutes} dakika</strong> sonra.`;
                    }
                } else {
                    message = "Bugün için yemek saati bitti.";
                }
            }

            document.getElementById("timer").innerHTML = `${message} <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>`;
        }

        setInterval(updateTimer, 1000);
        updateTimer();