<script setup> 

</script>

<template>
<div class="formatting-text">

<h2>IMPORTANT NOTE:</h2>
<p>The preprocessing script replaces single quotes (「」) with superscript quotation marks (""), and double quotes (『』) with same-line quotation marks («»). Take this into account while formatting the text as per the rules below.</p>

<h2>General formatting rules:</h2>
<h3>General</h3>
<ul>
   <li>Use double line breaks every time there's a line break in the JP text</li>
   <li>Oxford commas (e.g.: "X, Y, and Z") shall be used according to context, if dramatic pauses feel necessary or befitting the moment.</li>
   <li>Names ending in "s" with a possessive particle in front MUST have the "s" in the possessive particle (e.g.: Cecilus's, Louis's). This is valid, see <a href="https://www.grammarly.com/blog/possessive-noun/">this link</a>. The idea is to have it as is spoken.</li>
   <li>Ellipses (e.g.: "......") if longer than 1, should be reduced to 1 like this "…", there are very rare exceptions to this rule, such as when Tappei is using DOZENS of ellipses.</li>
   <li>Ellipses are to be rendered as a single character "…" rather than 3 periods ("...")</li>
   <li>Punctuation changes may occur in the following cases:
       <ul>
           <li>"X。…Y" -&gt; "X… Y"</li>
           <li>"X? …Y" -&gt; "X…? Y"</li>
           <li>"X! …Y" -&gt; "X…! Y"</li>
       </ul>
   </li>
   <li>Keep the punctuation when possible, particularly stuff like the ". ――", "――,", and whatnot.</li>
   <li>The JP text might show something like "--", which indicates the need for "――" in the EN translation.</li>
   <li>Em-dashes without preceding/following punctuation usually have a space right after (e.g.: "Blah blah―― blah blah". "Stuff stuff. ――Stuff stuff").</li>
   <li>Convention is usually to keep things as they are around the em-dashes unless it's straight-up impossible to make it sound well. Tappei uses the em-dashes a whole lot for stuff like "roundabout description of event/person-- contradiction or explanation", so we try and replicate that as best as possible. In character lines, it's more to convey a pause longer than a full-stop.</li>
   <li>Em-dashes are to be rendered with the following characters: ――</li>
   <li>Numbers in narration and speech should be written in full (e.g.: "five" instead of "5".</li>
   <li>When referring to a named physical building at a specific location, capitalize its name.</li>
   <li>An example would be the City Hall of Guaral, in the context of the chapters that take place there.</li>
   <li>Be sure that any instances of "△▼△▼△▼△" are center aligned. These typically only occur at the start of a new chapter part.</li>
</ul>

<h3>For speech:</h3>
<ul>
   <li>For dialogues that are「Dialogue, 『Quote』」please use the following format:<br>
       <ul><strong>Speaker Name: [Dialogue, "Quote"]</strong></ul>
   </li>
   <li>For dialogues that are:『Dialogue, 『Quote』』please use the following format:<br>
       <ul><strong>Speaker Name: [Dialogue, "Quote"]</strong></ul>
   </li>
   <li>For dialogues that are embedded into narration, you have an option of either writing the narration out, and using "Dialogue" to represent the embedded dialogue, or to move the dialogue down to the speaker's next sentence, if possible.</li>
   <li>For styling the speech of specific characters, check the Character Index, after the Glossary.</li>
   <li>If anyone uses Engrish in dialogue, and another character hears it, please underline the Engrish word.</li>
   <li>For proofreaders - wrap the Engrish expression with underline tags (&lt;u&gt;&lt;/u&gt;) when proofing, to highlight them for when the post is made</li>
   <li>In the WCT post, use &lt;/span&gt;&lt;span style="text-decoration: underline;"&gt;&lt;span style="font-weight: 400;"&gt;XXX&lt;/span&gt;&lt;/span&gt;&lt;span style="font-weight: 400;"&gt; to underline these words.</li>
   <li>Terminology that is written in 『』 should be one of the two:
       <ul>
           <li>If they are keywords, they should be capitalized (except connectors), and the double quote marks deleted. Examples:
               <ul>
                   <li>『嫉妬の魔女』- Witch of Envy</li>
                   <li>『インビジブル • プロヴィデンス』- Invisible Providence</li>
               </ul>
           </li>
           <li>If they are common words, they should be put in English quotation marks.
               <ul>
                   <li>『夢物語』 - "pipe dream"</li>
                   <li>『人間』- "human"</li>
                   <li>『資源』- "resources"</li>
               </ul>
           </li>
       </ul>
   </li>
   <li>Exceptions:
       <ul>
           <li>『死』- Death</li>
           <li>『記憶』- Memories</li>
           <li>『名前』- Names</li>
       </ul>
   </li>
   <li>For crossdressing characters, use "she/her" for those unaware (such as Jamal, Todd, etc…), "he/him" for those who are aware. Same logic goes for any female crossdresser that might appear in the story.</li>
   <li>Be mindful of the context, Subaru calling Flora/Flop a "he" in front of, say, Jamal, would be very odd.</li>
   <li>For a lone small っ that isn't followed by any text, "hk" is recommended. But if it's preceded by text I.E. 「なっ!?」please use a dash - to cut off the word or sentence in the middle where appropriate instead.</li>
   <li>For case in which characters are stuttering their speech (check for lone syllables before a comma, following by a full word, e.g.: "", ""), use "X-x" as a convention (e.g.: "T-that", "Y-you"). If the stuttered word is the first in a sentence, capitalize only the first letter (see previous example).</li>
   <li>There are some instances in which characters elongate their speech, but the way this is done in Japanese is different.
       <ul>
           <li>Elongation with vowels - add number of extra vowels plus one:
               <ul>
                   <li>いやぁ - "weeell"</li>
                   <li>そうですねえ - "isn't iiit?"</li>
               </ul>
           </li>
           <li>Elongation with em-dashes and vowel - add number of dashes as vowels plus one and til-de at the end:
               <ul>
                   <li>レムって、だーぁれのこと？- "Whooo~ is Rem?"</li>
                   <li>所持者の未来の一部はわかるようになっているねーぇ - "But it does reveal a portion of the owner's fuuuture~"</li>
               </ul>
           </li>
           <li>Elongation with til-de at the end - only keep the til-de:
               <ul>
                   <li>"あらあら~" - "Oh my~"</li>
                   <li>"きゃあ~" - "Kyaa~"</li>
               </ul>
           </li>
       </ul>
   </li>
</ul>

<h3>For speaker assignment:</h3>
<ul>
   <li>If it is the first time a character is coming into a scene, consider assigning their speech as "???" until the narration identifies them. If they're identified by a generic moniker (e.g.: "woman", "child", "young man") before being identified by name, use that until the name's name is mentioned in narration.</li>
   <li>For crossdressing characters, label their speech using their real names unless the POV is slanted through someone's lens. Same logic goes for any female crossdresser that might appear in the story.</li>
   <li>For lines spoken by more than one person (and if it's not everyone in the scene), use "A, B &amp; C: []".</li>
</ul>

<h3>For narration:</h3>
<ul>
   <li>Narration is to be rendered almost exclusively in third-person; only in very few cases should it be done in first-person (the use of 自分 is NOT an indicator of first-person narration)</li>
   <li>Use contractions ("he'd" / "would've" / "hadn't" / etc) only when the scene is light-hearted/not serious. Tension and graveness feels better conveyed when contractions aren't used in the narration.</li>
   <li>There may be a few exceptions for this, however. One of which was the Sirius scene in Arc 5 Chapter 19, in which using contractions heightens the intended dissonance between events and actions.</li>
   <li>Engrish in narration is often ignored, and so is not marked with an underline.</li>
   <li>When speech is embedded in narration, use "" to distinguish it from the rest.</li>
   <li>The tenses to use for conveying current actions, feelings or absolute truths in narration are the Past and Past Continuous tenses.</li>
   <li>The tenses to use for conveying past actions or feelings in narration are the Past Perfect and Past Perfect Continuous tenses.</li>
   <li>The tenses to use for conveying future or possible actions or feelings in narration are the Past Future, Past Future Continuous, Past Future Perfect and Past Future Perfect Continuous tenses.</li>
   <li>For crossdressing characters, use "he/her" pronouns unless the POV is slanted through the eyes of someone unaware of their crossdressing status.</li>
   <li>This is because the narration more often than not uses "彼" (gender-neutral) over "彼女" (female-specific) for these characters, possibly because the "normal" POV is Subaru's.</li>
</ul>
<br>
<p style="text-align: center;">△▼△▼△▼△</p>
</div>
</template>

<style scoped>
.formatting-text {
    font-size: 1.2rem;
    color: var(--formatting-text-color);
}

@media screen and (max-width: 600px) {
    .formatting-text {
        font-size: 1rem;
        transition: font-size 0.5s ease;
    }
    
}

h2, h3 {
    padding-top: 1em;
}

</style>