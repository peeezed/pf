class Metronome {
  constructor(tempo = 120) {
    this.audioContext = null;
    this.noteLength = 0.05; // length of the note
    this.notesInQueue = []; // notes that have been put into web audio and being ready to play {note, time}
    this.currentQuarterNote = 0; // last scheduled note
    this.tempo = tempo; // bpm
    this.lookahead = 25; // how frequently to call scheduling function (miliseconds)
    this.schduleAheadTime = 0.1 // how far ahead to schedule the actual audio (seconds)
    this.nextNoteTime = 0.0; // how long until the next note
    this.isRunning = false;
    this.intervalID = null;
  }

  nextNote() {
    // Advance current note and time by a quarter note
    var secondsPerBeat = 60.0 / this.tempo;
    this.nextNoteTime += secondsPerBeat; // adds beat length to last beat time
    this.currentQuarterNote++; // advance to beat number and wrap it to zero once it is 4
    if(this.currentQuarterNote == 4) {
      this.currentQuarterNote = 0;
    }
  }

  scheduleNote(beatNumber, time) {
    // this pushes the note to the playing queue even if we arent playing to negate lag
    this.notesInQueue.push({note: beatNumber, time:time});

    // creating sound oscillator
    const osc = this.audioContext.createOscillator();
    const envelope  = this.audioContext.createGain();

    osc.frequency.value = 800;

    // i am not hundred percent sure what this line does, but it changes sound to be more low and full and thicc and...

    envelope.gain.value = 1;
    envelope.gain.exponentialRampToValueAtTime(1, time + 0.001);
    envelope.gain.exponentialRampToValueAtTime(0.001, time + 0.02);

    osc.connect(envelope);
    envelope.connect(this.audioContext.destination)
    
    osc.start(time);
    osc.stop(time + this.noteLength);
  }

  scheduler() {
    // when there are notes that will need to play before the next interval, schedule them and advance the pointer
    while (
      this.nextNoteTime < 
      this.audioContext.currentTime + this.schduleAheadTime
    ) {
      this.scheduleNote(this.currentQuarterNote, this.nextNoteTime);
      this.nextNote();
    }
  }

  start() {
    if (this.isRunning) return;

    if (this.audioContext==null) {
      this.audioContext = new(window.AudioContext || window.webkitAudioContext)();
    }

    this.isRunning = true;
    this.currentQuarterNote = 0;
    this.nextNoteTime = this.audioContext.currentTime + this.noteLength;

    this.intervalID = setInterval(() => this.scheduler(), this.lookahead)
  }

  stop() {
    this.isRunning = false;
    clearInterval(this.intervalID);
  }

  startStop() {
    if (this.isRunning){
      this.stop();
    } else {
      this.start();
    }
  }
}