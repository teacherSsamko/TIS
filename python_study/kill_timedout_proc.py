# loop until all processes finish (or are killed)
	while True:

		# run commands
		if cmdInGen:
			for i in range(maxProc):
				if procArray[i] is None:
					try:
						task = cmdGen.next()
						procArray[i] = _ProcHandlerCmd(task, timeout)  # run process
						counter += 1
						print('Running "%s" cmd: %s' % (counter, task.cmd))
					except StopIteration:
						cmdInGen = False  # there are no processes to be run

		# sleep for a while
		time.sleep(timeStep)

		# check for finished processes and processes passed timeout
		for i in range(maxProc):
			ph = procArray[i]
			if ph is not None:  # there is a process in the slot
				if ph.process.poll() is None:
					# process running
					ph.incRuntime(timeStep)
					if ph.isTimeOut():
						# process over time, kill it!
						ph.process.kill()
						print("Process (%s): %s killed! (after %ss)" % (ph.getPid(), ph.cmd, ph.runtime))
						failList.append((ph.cmd, 9, ph.runtime, ph.getPid()))
						procArray[i] = None  # free slot
				else:
					# process finished
					ph.process.wait()
					if ph.process.returncode != 0:
						print('Process(%s): "%s" ended with return code: "%s' % (
							ph.getPid(), ph.cmd, ph.process.returncode))
						failList.append((ph.cmd, ph.process.returncode, ph.runtime, ph.getPid()))
					procArray[i] = None  # free slot

		# finish if no process is running and there is not process to be run
		if len(set(procArray.values())) == 1 and not cmdInGen:
			break

	return failList