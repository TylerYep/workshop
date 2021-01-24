## Big endian's advantage:

- Easier for (most) human to read when examining memory values. This sometimes also
  applies to serializing/deserializing values when communicating with networks.

- Easier sign checking (by checking the byte at offset 0)

- Easier comparison: useful in arbitrary-precision math, as numbers are compared from
  the most significant digit. But this is less important, because it’s not a common
  operation

- No need for endianness conversion when sending/receiving data to/from the network.
  This is less useful because network adapters can already swap bytes and copy them to
  memory in the correct order without the help of the CPU, and most modern CPUs have the
  ability to swap bytes themselves

## Little endian's advantage:

- Easier parity checking (by checking the byte at offset 0 we can see that it’s odd or
  even)

- Easier for some people to read: Arabic, Hebrew and many other languages write from
  right to left so they may read numbers in little-endian order. Some languages also
  read number values in little-endian order (like 134 as 4 units, 3 tens and 1 hundred),
  so it’s easier to know how big the current digit is. That means the thousand separator
  is less useful to them, as we immediately know how big the current digit is

- Natural in computation

  - Mathematics operations mostly work from least to most significant digit, so it's
    much easier to work in little-endian

  - This is extremely useful in Arbitrary-precision arithmetic (or any operations that
    are longer than the architecture's natural word size like doing 64-bit maths on
    32-bit computers) because it would be much more painful to read the digits backwards
    and do operations

  - It’s also useful in situations like in case a computer with limited memory bandwidth
    (like some 32-bit ARM microcontrollers with 16-bit bus, or the Intel 8088 with
    16-bit register but 8-bit data bus). Now the 32-bit CPU can do math 16 bits at a
    time by reading a halfword at address A, add it while still reading the remaining
    halfword at A+2 then do the final add instead of waiting for the two reads to be
    finished then adding from the LSB

- Always reads as the same value if reading in the size less than or equal to the
  written value.

  - For example 20 = 0x14 if writing as a 64-bit value into memory at address A will be
    14 00 00 00 00 00 00 00, and will always be read as 20 regardless of using 8, 16,
    32, 64-bit reads (or actually any reads with length <= 64 at the address A like 24,
    48 or 40 bits). This can be extended to arbitrarily longer types.

  - In big-endian system you have to know in which size you have written the value, in
    order to read it correctly. For example to get the least significant byte you need
    to read at byte A+n-1 (with n is the length in bytes of the write) instead of A.

  - This property also makes it easy to cast the value to a smaller type like int32_t to
    int16_t because the int16_t value will always lie at the beginning of int32_t.
