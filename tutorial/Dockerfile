FROM neurodesktop:latest

# Clone the pipelines-community repository
RUN mkdir -p ~/git

ADD requirements.txt /requirements.txt
# Install the pipelines-community repository
RUN pip install -r /requirements.txt
RUN python -m bash_kernel.install

