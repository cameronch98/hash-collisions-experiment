# Hash Collisions Experiment

A program to run experiments on the differences between breaking weak and strong collision resistance properties of the SHA256 hash algorithm. The program is set to run 100 trials of either test, and is configured to use 5 alphanumeric characters as input and compare only the first 24 bits / 6 hex characters (to make things computationally feasible). Individual trials and overall attempt averages are reported.

### MacOS/Linux

It is highly recommended to run this in a terminal/terminal emulator instead of through an IDE. First, clone the repository or download/extract the files. Then, it is recommended to go to the project directory and create a virtual environment as follows: 

```
python<version> -m venv <name-for-venv>
```

Then, we need to activate the venv by running:

```
source <name-for-venv>/bin/activate
```

Now that the virtual environment is enabled in the terminal, we need to install the packages required by the program that reside in requirements.txt. To do so, we can run the following command:

```
pip install -r requirements.txt
```

To run the weak collision experiment, we can enter one of the following:

```
python weak_collision.py
```
```
python3 weak_collision.py
```
```
<name-for-venv>/bin/python weak_collision.py
```

Similarly, to run the strong collision experiment, we can enter one of the following:

```
python strong_collision.py
```
```
python3 strong_collision.py
```
```
<name-for-venv>/bin/python strong_collision.py
```

# Usage
Once one of the experiments begin, trials will begin to come in showing the two different byte strings that mapped to the same hash prefixes, as well as the number of attempts it took to find a match. Once the 100 trials have completed, the average number of attempts is reported.
