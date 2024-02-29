# kakaoo


# Academic Course Scheduler

kakaoo is a Django-based web application designed to facilitate the scheduling of university courses for a specific major throughout the week. Users can add courses and professors, link them together, and schedule them accordingly.

## Algorithm

This software utilizes two key algorithms to optimize lesson scheduling:

1. **Graph Coloring Algorithm**: This mathematical algorithm is used to group lessons that can be presented in the same section. Each group represents a color.

2. **Genetic Algorithm**: This algorithm is used to arrange the groups of lessons across the days of the week. It works by generating a population of possible schedules. aiming to find the most optimal schedule.

By combining these algorithms, the software can effectively avoid scheduling conflicts and distribute lessons evenly throughout the week.

## Features

- Add and manage courses and professors.
- Link courses with professors.
- Schedule courses throughout the week.
- Built with Python and Django.

## Installation

Before you start, ensure you have installed the latest version of Python and pip. This project also requires Django. You can install Django using pip:

```
pip install Django
```

## Usage

Follow these steps to get the application up and running:

Clone the repository
```
git clone https://github.com/mehdee81/kakaoo
```
Navigate to the project directory
```
cd .\kakaoo\
```
```
cd .\app\
```
Make migrations for the 'scheduler' app
```
Python .\manage.py makemigrations scheduler
```
Apply the migrations
```
python .\manage.py migrate
```
Run the server
```
python .\manage.py runserver
```

Now, you can access the application at `http://127.0.0.1:8000/` in your web browser.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the terms of the MIT license. See the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions, feel free to open an issue or submit a pull request.

You can contact me via email at [momeni.mpost@gmail.com](momeni.mpost@gmail.com).
