TODO:
	* {Endpoint} Create Endpoint function
		* Input: <VidBuff>, <Metadata Object>
		* Output: <SQS Queue> (For development, <Log Files>)
		* Process:
			1. Listen on Port
			2. Revieve data
			3. Check <Tag>
			4. Store into relevent <Log File>
	* {API Connection Proxy} Create Connection Handler Class (<Connection>) [Singleton]
		* Object: Pool of connections to Endpoint
		- Handle opening and safe closing of connections
	* {Metadata} Create Tagging system (<BufferIdSystem>)
		* Objects: Tag List (<Tag>)
		* Input: Given <Tag>, <Date+Time>, <IP Address>
		* Output: <Metadata Object>
		* Process:
			1. Hashing <Date+Time> and <IP Address>
			2. Compiling it into a Object
	* {Asynchronous Function} Make asynchronous function to send video frames
		* Input: <Tag>, <VideoBuff>, <Connection>
		* Output: <Success | Failure> & Relevant Metadata
		* Process:
			1. Read in video frames
			2. Append tag
			3. Create Hash + Metadata
			4. Send data through <Connection>
			5. return <Success | Failure>
	* Lease with Armin for Unit Testing
	* Jono & Badat -> Video Buffer Object (<VideoBuff>)
	* Jono & Badat -> Tags (<Tag>)

Plan:
	1. API Connection Proxy (A) & Metadata (B)
	2. Endpoint (C) & Asynchronous Function (B)
